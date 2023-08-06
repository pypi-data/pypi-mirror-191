from dataclasses import dataclass
from keyframed import Curve, ParameterGroup, SmoothCurve
from keyframed.utils import DictValuesArithmeticFriendly
from keyframed.curve import CurveBase
from collections import UserDict
from itertools import accumulate
from numbers import Number


from keyframed import SmoothCurve
from keyframed.curve import CurveBase


class Prompt:
    def __init__(
        self,
        text,
        weight=1,
        encoder=None,
    ):
        self.text=text
        if not isinstance(weight, CurveBase):
            weight = SmoothCurve(weight)
        self.weight=weight
        self.encoder=encoder

    @property
    def cond(self):
        if hasattr(self, '_cond'):
            return self._cond
        if self.encoder is not None:
            self._cond = self.encoder(self.text)
            return self._cond
        return None # just to be explicit

    def __getitem__(self, t):
        outv = dict(
            weight=self.weight[t],
            text=self.text,
            cond=self.cond
        )
        if outv['weight'] == 0:
            return {}
        return outv
        

#class SceneSettings(ParameterGroup):
class SceneSettings(UserDict):
  pass

def resolve_for_time_slice(obj, t, weight=1):
  """
  recursively resolves CurveBase objects for the given t, where it can find them.
  """
  if weight==0:
    return None
  if isinstance(obj, CurveBase):
    return obj[t] * weight
  elif isinstance(obj, Prompt):
    outv = obj[t]
    #outv[0]['weight'] = outv[0]['weight'] * weight
    if outv:
        outv['weight'] = outv['weight'] * weight
        return outv
    else:
        return None
  elif isinstance(obj, list):
    #return [resolve_for_time_slice(o, t, weight) for o in obj]
    outv = []
    for elem in obj:
        item = resolve_for_time_slice(elem, t, weight)
        if item is not None:
            outv.append(item)
    return outv
  elif isinstance(obj, dict) or isinstance(obj, UserDict):
    return {k:resolve_for_time_slice(v, t, weight) for k,v in obj.items()}
  elif isinstance(obj, Number):
      return obj * weight
  else:
    #print(type(obj))
    #print(obj)
    return obj

from abc import ABC, abstractmethod

class SceneBase(ABC):
    @property
    def loop(self) -> bool:
        if hasattr(self, '_loop'):
            return self._loop
        return False
    @property
    def label(self) -> str:
        if hasattr(self, '_label'):
            return self._label
        return None

    @property
    def priority(self) -> Number:
        if hasattr(self, '_priority'):
            return self._priority
        return 0

    @property
    def start(self) -> Number:
        if hasattr(self, '_start'):
            return self._start
        return 0
        
    @property
    def end(self) -> Number:
        if hasattr(self, '_end'):
            return self._end
        return None

    @property
    def duration(self) -> Number:
        if self.end is not None:
            return self.end - self.start
        return None


    def is_active(self, t, priority=None) -> bool:
        if priority is not None:
            if self.priority<priority:
                return False
        if self.loop:
            return True
        if not (self.start <= t):
            return False
        if self.end is not None:
            if self.end <= t:
                return False

        return True

    # not sure how I feel about this. I think I want to expose the weight attribute so it can be modified directly.
    # may just need to define property setters and getters
    @property
    def weight(self) -> CurveBase:
        if not hasattr(self, '_weight'):
            self._weight = SmoothCurve(1)
        return self._weight

        


class Scene(SceneBase):
  """
  Defines a locally 0-indexed reference frame of settings.
  the priority attribute can be used to define how settings derived from 
  different scenes are combined.
  """
  def __init__(
      self,
      settings=None,
      label=None,
      priority=0,
      start=0,
      end=None,
      weight=1,
      loop=False,
  ):
      self._priority = priority
      if settings is None:
        settings = SceneSettings()
      if not isinstance(settings, SceneSettings):
        settings = SceneSettings(settings)
      self.settings = settings
      self._start=start
      self._end=end
      if not isinstance(weight, CurveBase):
          weight = SmoothCurve(weight)
      self._weight=weight
      self._loop = loop

  def __getitem__(self, t) -> dict:
      if self.loop:
          t = t % self.duration
      if not self.is_active(t):
          return {}
      t -= self.start
      wt = self.weight[t]
      return resolve_for_time_slice(obj=self.settings, t=t, weight=wt)


# this should inherit from a parentclass common to Scene and ScenesCollection
class SceneSequence(SceneBase):
    def __init__(
        self,
        scenes=None,
        durations=None,
        transition_duration=None,
        loop=False,
        start=0,
        end=None,
    ):
        self.scenes=scenes
        self._loop = loop
        if durations:
            self.apply_scene_durations(durations, transition_duration)
        self._start = start
        if (end is None) and (durations is not None):
            end = sum(durations)
        self._end = end

    def apply_scene_durations(self, durations, transition_duration):
        end_frame = list(accumulate(durations))
        #start_frame = [0] + [i-1 for i in end_frame[:-1]]
        start_frame = [0] + [i for i in end_frame[:-1]]
        for i, (scene, start, end) in enumerate(zip(self.scenes, start_frame, end_frame)):
            print(i, start, end)
            td = transition_duration
            if (td is None) or (i==0):
                scene._start=start
                scene._end=end
            else:
                # 1. shrink previous scene into transition
                prev_scene = self.scenes[i-1]
                # nb: converted to local frame's time
                end_old = prev_scene.end
                prev_scene._end = end_old + td
                delta = prev_scene.end - prev_scene.start
                e0 = delta
                e1 = delta - td
                prev_scene.weight[e1] = prev_scene.weight[e1] # ensure we have a keyframe at e1 whose value is whatever it would've been anyway
                prev_scene.weight[e0] = 0

                # 2. extend current scene into transition
                scene._end=end
                scene._start = end_old #start - td
                scene.weight[td] = scene.weight[td] # make sure we have a keyframe at td whose value is whatever it would've been anyway
                print("hmm...", i, scene[scene.start])
                scene.weight[0] = 0 
                

    def __getitem__(self, t):
        if self.loop:
            t = t % self.duration # uh... sure. this is gonna break if start > 0 though.
        settings = {}
        for scene in self.scenes:
            if not scene.is_active(t):
                continue
            self._update(settings, scene, t)
        return settings

    def __setitem__(self, k, v):
        self.settings[k] = v

    def _update(self, settings, scene, t):
        candidates = scene[t]
        if candidates:
            for k in candidates.keys():
                if k not in settings:
                    settings[k] = candidates[k]
                else:
                    settings[k] += candidates[k]


class ScenesCollection(SceneBase):
  def __init__(
      self,
      scenes=None,
      durations=None,
  ):
      self.scenes=scenes
      if durations:
          self.apply_scene_durations(durations)

  # this function still needs a test case
  def apply_scene_durations(self, durations):
    end_frame = list(accumulate(durations))
    start_frame = [0] + [i for i in end_frame[:-1]]
    for scene, start, end in zip(self.scenes, start_frame, end_frame):
        scene._start=start
        scene._end=end
  def __getitem__(self, t):
      settings = {}
      settings_priorities = {} # tracks the priority level for the current value of each associated setting
      for scene in self.scenes:
          # to do: incorporate priority test here..?
          if not scene.is_active(t):
              continue
          self._update(settings, settings_priorities, scene, t)
      return settings

  def __setitem__(self, k, v):
      self.settings[k] = v

  def _update(self, settings, settings_priorities, scene, t):
          return self._update_overrides(settings, settings_priorities, scene, t)

  def _update_overrides(self, settings, settings_priorities, scene, t):
      """
      handles internal logic for combining or overriding parameters.
      """
      candidates = scene[t]
      for k in candidates.keys():
        if (settings_priorities.get(k, scene.priority) < scene.priority) or (k not in settings_priorities):
            settings_priorities[k] = scene.priority
            settings[k] = candidates[k]
        elif settings_priorities.get(k, scene.priority) == scene.priority:
            settings[k] = settings[k] + candidates[k] 
  

