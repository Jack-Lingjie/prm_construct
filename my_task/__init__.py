def get_task(name):
    if name == 'prm':
        from my_task.prm import PRM
        return PRM()
    # elif name == 'text':
    #     from tot.tasks.text import TextTask
    #     return TextTask()
    # elif name == 'crosswords':
    #     from tot.tasks.crosswords import MiniCrosswordsTask
    #     return MiniCrosswordsTask()
    else:
        raise NotImplementedError