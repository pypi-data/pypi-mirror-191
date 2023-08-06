def combinations(*args):
    def __combinations(res, a):
        for r in res:
            for x in a:
                yield r + [
                    x,
                ]

    result = None
    for arr in args:
        if result is None:
            result = (
                [
                    _,
                ]
                for _ in arr
            )
        else:
            result = __combinations(result, arr)

    return result
