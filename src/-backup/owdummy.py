def owdummy(ow, times):

    def _get_data_safe():
        try:
            return _ow.read('/Ctl_FrontDoor/sensed.BYTE').strip()
        except:
            return ''

    _ow = ow

    while True:
        yield
        for _ in range(times):
            _get_data_safe()
