import time


def time_counter(func):
    def inner_func(*args, **kwargs):

        TIME_DECIMAL_PRECISION = 6

        # measure total time
        start_time_ns = time.time_ns()
        returned_value = func(*args, **kwargs)
        end_time_ns = time.time_ns()

        total_time_sec = (end_time_ns - start_time_ns) / pow(10, 9)
        total_time_sec = round(total_time_sec, TIME_DECIMAL_PRECISION)

        print(f"[INFO] Total time: {total_time_sec} seconds")

        return returned_value

    return inner_func
