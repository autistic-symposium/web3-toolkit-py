# -*- coding: utf8 -*-

import sys

import logging as l

import src.encoder as enc
from src.utils import get_boundary_limits


class EPen(object):

    def __init__(self):
        self.boundary = enc.get_boundary_limits('enc')
        self.color = None
        self.pen_location = None
        self.is_pen_down = None

    def _parse_clear(self):
        """
        Runs clear operations and prints CLEAR STDOUT.
        """
        self.pen_location = [0, 0]
        self.color = [0, 0, 0, 255]
        self.is_pen_down = False
        print('CLR;')

    def _parse_pen_state(self, substr):
        """
        Sets pen to be UP or DOWN and prints PEN STATE STDOUT.
        
        Arguments:
            substr {str} -- parameters for this opcode, which is
            either 0 (for pen up) or any other (for pen down)
        """
        if substr:
            pen_state = enc.run_decoder(substr)
        else:
            l.error('Could not parse pen state string {}'.format(substr))

        if pen_state == 0:
            if self.is_pen_down:
                self.is_pen_down = False
                print('PEN UP;')
        else:
            if not self.is_pen_down:
                self.is_pen_down = True
                print('PEN DOWN;')

    def _parse_color(self, substr):
        """
        Sets pen color and prints COLOR SET STDOUT.
        
        Arguments:
             substr {str} -- RGBA parameters for this opcode, 
             which is represented by four integers in the range 
             [0, 255] defining colors (red, green, blue) and alpha.
        """
        red = enc.run_decoder(substr[:4])
        green = enc.run_decoder(substr[4:8])
        blue = enc.run_decoder(substr[8:12])
        alpha = enc.run_decoder(substr[12:16])

        self.color = [red, green, blue, alpha]
        print('CO {0} {1} {2} {3};'.format(*self.color))

    def _parse_pen_move(self, substr):
        """
        Parses a substring of parameters and usex this data 
        as pair of coordinates to move the pen inside the
        square boundary limit.
        
        Arguments:
            substr {str} -- (x,y) pairs with directions to where
                the pen should move to (at least one pair).
        
        Returns:
            i - an integer indicating how much of the input
            substring was used in this opcode.
        """
        i = 0
        move_list = []

        while i < len(substr):
            try:
                # Ends if find another opcode.
                if substr[i:i+2] in set(['F0', '80', 'A0']):
                    break

                if len(substr[i:]) > 8:
                    x_coords = enc.run_decoder(substr[i:i+4])
                    y_coords = enc.run_decoder(substr[i+4:i+8])
                    move_list.append([x_coords, y_coords])
                    i += 8
                else:
                    break

            except (KeyError, ValueError) as e:
                l.error('Ill-formated MV data: {}'.format(e))
        
        self._move_pen(move_list)
        return i

    def _print_mv(self, cmd_list=None):
            """ 
            Prints MV PEN STDOUT. If a string with a list of commands
            is given, print that instead of pen_location.

            Arguments:
                cmd_list {list (optional)} -- a list with pairs of 
                (x, y) coordinates.
            """
            if cmd_list:
                cmd_str = ' '.join(cmd_list)
                print('MV {};'.format(cmd_str))
            else:
                print('MV ({0}, {1});'.format(self.pen_location[0], self.pen_location[1]))
    
    def _fix_boundary(self, coord):
        """
            Check if the coordinate exceeds
            the boundary limit, returning this 
            value in that case.
        
        Arguments:
            coord {int} -- x or y coordinate.
        
        Returns:
            An integer representing the fixed coordinate.
        """
        if coord < self.boundary[0]:
            return self.boundary[0]
        elif coord > self.boundary[1]:
            return self.boundary[1]
        else:
            return coord

    def _fix_boundaries(self, x, y):
        """
            Checks if a set of (x, y) coordinates
            exceeds the boundary limits, returning  
            a fixed (x, y) pair.
        
        Arguments:
            coord {list} -- (x, y) coordinates.

         Returns:
            A (x, y) pair representing the fixed coordinates.
        """
        return self._fix_boundary(x), self._fix_boundary(y)

    def _is_inside_boundary(self, xymove=None):
        """
        Checks whether a set of coordinate is inside 
        of the boundary, returning True if the case, 
        or False otherwise.

        Arguments:
            xymove {tuple} - (x, y) tuple.
        
        Returns:
            True if the coordinates were fixed, False
            otherwise.
        """
        if xymove is None:
            xymove = self.pen_location

        x_fix = self._fix_boundary(xymove[0])
        y_fix = self._fix_boundary(xymove[1])
        return (xymove[0] == x_fix and xymove[1] == y_fix)

    def _is_on_the_boundary(self, xymove=None):
        """
        Checks whether a coordinate is on the boundary, 
        returning True if the case, or False otherwise.

        Arguments:
            xymove {tuple} - (x, y) tuple.

        Returns:
            True if any of the (x, y) coordinates are
            on the boundary, False otherwise.
        """
        if xymove is None:
            x, y = self.pen_location

        return x == self.boundary[0] or x == self.boundary[1] or \
               y == self.boundary[0] or y == self.boundary[1] 


    def _get_next_position(self, xymove):
        """
        Givens a move coordinates (x, y), returns the next
        destination coordinate for the pen. 

        Arguments:
            xymove {tuple} - (x, y) tuple.
        
        Returns:
            The next (x, y) coordinates to move the pen to.
        """
        return self.pen_location[0] + xymove[0], \
               self.pen_location[1] + xymove[1]

    def _move_pen(self, move_list):
        """
        Changes the location of the pen relative to its current location. 
        
        Arguments:
            move_list {list} -- list of coordinates to move the pen.
        """
        # Loop over the list of (x ,y) moves, adding them to 
        # a dictionary, together with a boolean False if x or y
        # is outside the limits.
        tablet_dict = {}
        for n, xymove in enumerate(move_list, 1):
            self.pen_location = self._get_next_position(xymove)

            if self._is_inside_boundary():
                tablet_dict[n] = [self.pen_location, True]
            else:
                tablet_dict[n] = [self.pen_location, False]


        # Find the positions and print it as pen down.
        if self.is_pen_down:
            cmd_list = []

            for i in sorted(tablet_dict): 
                x = tablet_dict[i][0][0]
                y = tablet_dict[i][0][1]
                is_inside = tablet_dict[i][1]

                if is_inside:
                    cmd_list.append('({0}, {1})'.format(x, y))
                else:
                    break
            
            if cmd_list:
                self._print_mv(cmd_list)
            
            # It broke the boundary at some point.
            if i < len(tablet_dict):
                for item in range(i, len(tablet_dict)+1):
                    coords, is_inside = tablet_dict[item]
                    self.pen_location = self._fix_boundaries(coords[0], coords[1])
                    self._print_mv()
                    if item != len(tablet_dict):
                        if not is_inside:
                            if self.is_pen_down: 
                                self._parse_pen_state('4000')
                            else:
                                self._parse_pen_state('4001')
            else:
                coords, is_inside = tablet_dict[i]
                self.pen_location = self._fix_boundaries(coords[0], coords[1])
                if not is_inside:
                    self._parse_pen_state('4000')
                
        # Pen is up.
        else:
            last_position = tablet_dict[sorted(tablet_dict)[-1]][0]
            self.pen_location = self._fix_boundaries(*last_position)
            self._print_mv()

    def parse_stream(self, stream_str):
        """
        Parses a stream string and run its commands and their 
        adjacent parameters.
        
        Arguments:
            stream_str {str} - data stream of actions be taken.
        """
        i = 0

        while i < len(stream_str):

            # Opcode is CLEAR.
            if stream_str[i:i+2] == 'F0':
                l.debug('Parsing clear opcode...')
                self._parse_clear()
                i += 2
                
            # Opcode is SET PEN STATE.
            elif stream_str[i:i+2] == '80':
                l.debug('Parsing pen state opcode...')
                self._parse_pen_state(stream_str[i+2:i+6])
                i += 6

            # Opcode is SET COLOR. 
            elif stream_str[i:i+2] == 'A0':
                l.debug('Parsing color opcode...')
                self._parse_color(stream_str[i+2:i+18])
                i += 18

            # Opcode is MOVE PEN. 
            elif stream_str[i:i+2] == 'C0': 
                l.debug('Parsing pen move opcode...')
                i += 2 + self._parse_pen_move(stream_str[i+2:])
            
            # Opcode is not identified.
            else:
                l.debug('Non-identificated char: {}'.format(stream_str[i]))
                i += 1
