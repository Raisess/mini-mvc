import traceback

class Logger:
  class __Error:
    def __init__(self, title: str, trace: str, custom_message: str):
      self.title = title
      self.trace = trace
      self.custom_message = custom_message


  @staticmethod
  def Error(message: str, exception: Exception) -> None:
    error = Logger.__Format(message, exception)
    print(f"===> {message}")
    print(error.title)
    print(error.trace)

  @staticmethod
  def __Format(message: str, exception: Exception) -> __Error:
    title = exception.__str__()
    trace = "".join(traceback.format_tb(exception.__traceback__))
    return Logger.__Error(title, trace, message)
