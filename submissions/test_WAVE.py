from WAVE import WAVE


def execute_test_WAVE():
    wave_prefered = WAVE(1, './test/prefered.png', 'str')
    wave_preferred_value = wave_prefered.execute_metric()
    wave_not_prefered = WAVE(2, './test/leats_prefered.png', 'str')
    wave_not_preferred_value = wave_not_prefered.execute_metric()
    print('wave_preferred_value', wave_preferred_value)
    print('wave_not_preferred_value', wave_not_preferred_value)
    status = False
    if wave_preferred_value > wave_not_preferred_value:
        status = True
        
    if status:
        print('test passed')
        return 'test passed'
        
    return 'test not passed'
    