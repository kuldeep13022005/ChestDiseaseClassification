import os
import sys
from Respire.Logger import logging

def error_message_detail(error, error_detail=None):
    if error_detail is None:
        import sys
        error_detail = sys
    # Retreiving TraceBack information
    # exc_info() returns a tuple - (Exception type, Exception value, traceback)
    _, _, exc_tb = error_detail.exc_info()
    # Extracting file name, line number and error message
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_no = exc_tb.tb_lineno
        ermsg = f"Error in Script: {file_name} - Line: {line_no} - Message: {str(error)}" 
    else:
        ermsg = f"Error: {str(error)}"
    logging.info(ermsg)
    return ermsg

class CustomException(Exception):
    def __init__(self, ermsg, error_detail=None):
        super().__init__(ermsg)
        self.error_message = error_message_detail(
            ermsg, error_detail=error_detail)

    def __str__(self):
        return self.error_message