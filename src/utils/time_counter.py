import time
import pandas as pd


def time_counter(func):
    """
    This decorator should be only used on top of solve() function
    """
    def inner_func(self, *args, **kwargs):

        TIME_DECIMAL_PRECISION = 6


        # * measure total time
        start_time_ns = time.time_ns()
        returned_value = func(self, *args, **kwargs)
        end_time_ns = time.time_ns()

        total_time_sec = (end_time_ns - start_time_ns) / pow(10, 9)
        total_time_sec = round(total_time_sec, TIME_DECIMAL_PRECISION)

        df = pd.DataFrame(data = [{
            'name': self.instance.name,
            'vertices number': self.instance.dimension,
            'time [s]': total_time_sec,
            'cost': returned_value[0]
        }])

        self.output_df = pd.concat([self.output_df, df], ignore_index=True)


        print(f"[INFO] Total time: {total_time_sec} seconds")

        return returned_value

    return inner_func
