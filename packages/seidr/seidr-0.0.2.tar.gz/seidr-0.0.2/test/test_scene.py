from seidr.scene import Prompt, Scene, ScenesCollection, SceneSequence


def test_prompt():
    p = Prompt("foo bar")

def test_prompt_in_scene():
    p = Prompt("foo bar")
    s = Scene(settings={'prompt':p})
    #print(s[0], s[1], s[2])
    assert s[0] == {'prompt': {'weight': 1, 'text': 'foo bar', 'cond': None}}
    assert s[1] == {'prompt': {'weight': 1, 'text': 'foo bar', 'cond': None}}
    assert s[2] == {'prompt': {'weight': 1, 'text': 'foo bar', 'cond': None}}

def test_prompt_scene_offset():
    p = Prompt("foo bar", weight={0:1, 1:2})
    s = Scene(settings={'prompt':p}, start=1)
    #print(s[0], s[1], s[2])
    assert s[0] == {}
    assert s[1] == {'prompt': {'weight': 1, 'text': 'foo bar', 'cond': None}}
    assert s[2] == {'prompt': {'weight': 2, 'text': 'foo bar', 'cond': None}}

def test_multiprompt_scene():
    p0 = Prompt("foo bar", weight={0:1, 1:2})
    p1 = Prompt("baz", weight={0:3})
    s = Scene(settings={'prompts':[p0, p1]}, start=1)
    #print(s[0], s[1], s[2])
    assert s[0] == {}
    assert s[1] == {'prompts': [{'weight': 1, 'text': 'foo bar', 'cond': None}, {'weight': 3, 'text': 'baz', 'cond': None}]}
    assert s[2] == {'prompts': [{'weight': 2, 'text': 'foo bar', 'cond': None}, {'weight': 3, 'text': 'baz', 'cond': None}]}


from itertools import accumulate

def test_two_scene_schedule():
    p0 = Prompt("foo bar", weight={0:1, 1:2})
    p1 = Prompt("baz", weight={0:3})
    s1 = Scene(settings={'prompts':[p0, p1]})

    p2 = Prompt("crunch", weight={0:1})
    s2 = Scene(settings={'prompts':[p2]})

    scenes = [s1, s2]
    scene_durations = [5, 6]
    end_frame = list(accumulate(scene_durations))
    start_frame = [0] + [i for i in end_frame[:-1]]
    for scene, start, end in zip(scenes, start_frame, end_frame):
        print(start, end)
        scene.start=start
        scene.end=end

    for i in range(20):
        print(i, s1[i], s2[i])
    #raise
    
    scenes2 = SceneSequence([s1,s2])
    for i in range(5):
        print(i, s1[i], s2[i])
        print(i, scenes2[i]) 
        assert s1[i] == scenes2[i]
    for i in range(5, 11):
        assert s2[i] == scenes2[i]
    for i in range(11, 20):
        assert scenes2[i] == {}
    #raise

    #####################################

    # ok, this time: no behavioral crutch.
    p0 = Prompt("foo bar", weight={0:1, 1:2})
    p1 = Prompt("baz", weight={0:3})
    s1 = Scene(settings={'prompts':[p0, p1]})

    p2 = Prompt("crunch", weight={0:1})
    s2 = Scene(settings={'prompts':[p2]})

    #scenes3 = ScenesCollection([s1, s2], durations = [5, 6])
    scenes3 = SceneSequence([s1, s2], durations = [5, 6])
    for i in range(20):
        assert scenes2[i] == scenes3[i]

def test_overlapping_scenes():
    p0 = Prompt("foo bar", weight={0:1})
    s1 = Scene(settings={'prompts':[p0]}, end=5)

    p1 = Prompt("baz", weight={0:1})
    s2 = Scene(settings={'prompts':[p1]}, start=3)

    scenes = SceneSequence([s1, s2])
    for i in range(10):
      print(i, scenes[i])
      if 0 <= i < s2.start:
          assert scenes[i] == {'prompts': [{'weight': 1, 'text': 'foo bar', 'cond': None}]}
      elif i < s1.end:
          assert scenes[i] == {'prompts': [{'weight': 1, 'text': 'foo bar', 'cond': None}, {'weight': 1, 'text': 'baz', 'cond': None}]}
      else:
          assert scenes[i] == {'prompts': [{'weight': 1, 'text': 'baz', 'cond': None}]}

def test_scene_transition_propagates_to_prompt_weights():
    p0 = Prompt("foo bar", weight={0:1})
    s0 = Scene(settings={'prompts':[p0]})

    p1 = Prompt("baz", weight={0:1})
    s1 = Scene(settings={'prompts':[p1]})

    p2 = Prompt("crunch", weight={0:1})
    s2 = Scene(settings={'prompts':[p2]})

    scenes = SceneSequence([s0, s1, s2], durations=[50,50, 50], transition_duration=20)
    for i in range(0,150,10):
        print(i, scenes[i])

    assert scenes[0] == {'prompts': [{'weight': 1, 'text': 'foo bar', 'cond': None}]}
    assert scenes[50] == {'prompts': [{'weight': 1, 'text': 'foo bar', 'cond': None}, {'weight': 0, 'text': 'baz', 'cond': None}]}
    assert scenes[60] == {'prompts': [{'weight': 0.5000000000000001, 'text': 'foo bar', 'cond': None}, {'weight': 0.4999999999999999, 'text': 'baz', 'cond': None}]}
    assert scenes[70] == {'prompts': [{'weight': 1, 'text': 'baz', 'cond': None}]}
    assert scenes[100] == {'prompts': [{'weight': 1, 'text': 'baz', 'cond': None}, {'weight': 0, 'text': 'crunch', 'cond': None}]}
    assert scenes[110] == {'prompts': [{'weight': 0.5000000000000001, 'text': 'baz', 'cond': None}, {'weight': 0.4999999999999999, 'text': 'crunch', 'cond': None}]}
    assert scenes[120] == {'prompts': [{'weight': 1, 'text': 'crunch', 'cond': None}]}
    assert scenes[149] == {'prompts': [{'weight': 1, 'text': 'crunch', 'cond': None}]}


def test_prompt_collection():
    p0 = Prompt("foo bar", weight={0:1})
    s0 = Scene(settings={'prompts':[p0]})

    p1 = Prompt("baz", weight={0:1})
    s1 = Scene(settings={'prompts':[p1]})

    scene = ScenesCollection([s0, s1])
    print(scene[0])
    assert scene[0] == {'prompts': [{'weight': 1, 'text': 'foo bar', 'cond': None}, {'weight': 1, 'text': 'baz', 'cond': None}]}

def test_scene_transitions_between_sequences():
    pass

def test_tied_scenes():
    pass

def test_tied_sequences():
    pass

def test_scene_defaults():
    pass

def test_sequence_defaults():
    pass

def test_scene_settings_override_sequence_defaults():
    pass
