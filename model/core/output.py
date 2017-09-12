#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
# output.py:
#
# A mixin class to provide functionality for writing data.
#
# ------------------------------------------------------------------------------

import os
import sys
import re
import codecs

# ------------------------------------------------------------------------------
#
# Class Output
#
# ------------------------------------------------------------------------------
class Output():

    # --------------------------------------------------------------------------
    def output(self, txt, directory=""):

        # check if the view contains special output statement lines:
        # ">> [path] [comments]\n" which advise to output the following
        # data to a file location indicated by the [path] argument

        block     = ""
        file_name = ""
        for line in txt.splitlines():
            # determine new filename: ">> [filename] [comments]"
            match = re.match(">> ([^ ]*)(.*)", line)
            if match:
                # write the existing block
                if block != "":
                    self._output_block(directory, file_name, block)

                    # reset block and file name
                    block = ""

                # set new file name
                file_name = match.group(1)
            else:
                if block == "":
                    block = line
                else:
                    block += "\n" + line

        # write last block
        self._output_block(directory, file_name, block)

    # --------------------------------------------------------------------------
    def _output_block(self, directory, file_name, block):
        try:
            # write to stdout if no proper output file can be determined
            if (directory == "") or (file_name == "") or (not os.path.isdir( directory )):
                print(block)
                return

            # write to stdout if file points to a directory
            file_path = os.path.join(directory, file_name)

            if os.path.isdir( file_path ):
                print(block)
                return

            # ensure that the directory exists
            dir_path = os.path.dirname(file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # write block as text file
            with codecs.open(file_path, "w", "utf-8") as text_file:
                text_file.write(block)

        except IOError as exc:
            snippet_len = 500
            short_block = (block[ :snippet_len ] + "..") if len(block) > snippet_len else block
            print( "Error while writing to file {}: \n\n=== SNIPPET START (first {} chars)=== \n{}\n===SNIPPET END===".format(file_name, snippet_len, short_block))
