# -*- coding: utf-8 -*-


class BaseFsm(object):

    def __init__(self):
        pass

    def enter(self, obj, original_state, **kwargs):
        pass

    def execute(self, obj, original_state, **kwargs):
        pass

    def exit(self, obj, original_state, **kwargs):
        pass


class FsmManager(object):
    # 决定重新进入相同状态时，是否执行状态流函数
    _re_enter_flag = False

    def __init__(self):
        self.fms_handler = {}

    # 子类必须实现此方法，状态流合法返回None，否则返回error msg
    def _check_state_flow(self, obj, original_state, new_state, **kwargs):
        raise NotImplementedError()

    # 状态切换函数，需判断返回值
    def change_state(self, obj, original_state, new_state, **kwargs):
        # 状态无变化
        if original_state == new_state:
            if not self._re_enter_flag:
                return None
            if original_state in self.fms_handler and self.fms_handler[original_state]:
                handler = self.fms_handler[original_state]

                # 离开原状态
                res = handler.exit(obj, original_state, **kwargs)
                if res:
                    return res

                # 重新进入原状态
                res = handler.enter(obj, original_state, **kwargs)
                if res:
                    return res

                # 执行原状态
                res = handler.execute(obj, original_state, **kwargs)
                if res:
                    return res
            return None

        # 检测状态流转是否合法
        res = self._check_state_flow(obj, original_state, new_state, **kwargs)
        if res:
            return res

        if original_state in self.fms_handler and self.fms_handler[original_state]:
            # 离开原状态
            self.fms_handler[original_state].exit(obj, original_state, **kwargs)

        if new_state in self.fms_handler and self.fms_handler[new_state]:
            handler = self.fms_handler[new_state]

            # 进入新状态
            res = handler.enter(obj, original_state, **kwargs)
            if res:
                return res

            # 执行新状态
            res = handler.execute(obj, original_state, **kwargs)
            if res:
                return res

        return None
