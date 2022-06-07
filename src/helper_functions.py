#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" Final Project """
__author__="Tho Tran"

from math import sin, cos, sqrt, radians, atan2

def display_help():
    return('\n' + '-'*40 + ' Welcome to Pathfinder ' + '-'*40 + '\n' 
            + '\nYou can run the program from the command line, press the enter button to submit commands or inputs.'
            + '\nType the command "python final_project.py" to run the program.\n'
            + '\nThere will be a prompt that asks you to type "help" to get assistance' 
            + '\nor "start" to start the program. The commands are case sensitive.\n'
            + '\nNext, a list of landmarks will be displayed.'
            + '\nA prompt will appear and ask you to type a starting location from the list of landmarks.'
            + '\nAnother prompt will appear and ask you to type your destination from the list of landmarks.\n'
            + '\nPLEASE CHECK YOUR SPELLING OR AVOID ADDING EXTRANEOUS WHITESPACE, the program checks for spelling.\n'
            + '''\nNew landmark's data must be added to both Chicago_Landmarks.csv and CPD_Park_Arts.csv files.'''
            + '''\nNew park's data must be added to CPD_Park_Arts.csv file\n'''
            + '\n' + '-'*102 + '\n')

def check_user_input(user_input):
    if user_input == 'help':
        print(display_help())
    elif user_input == 'start':
        return True
    else:
        print('\nPlease enter a valid command: help OR start\n')

def check_spelling(user_location, user_dest, landmarks):
    if user_location not in landmarks or user_dest not in landmarks:
        return False
    return True

def display_landmarks(landmarks_dict):
    out = ''
    for key in landmarks_dict.keys():
        out = out + key + '\n'
    return out

def find_distance(source_node, dest_node):
    lon1 = source_node.long
    lat1 = source_node.lat
    lon2 = dest_node.long
    lat2 = dest_node.lat
    radius = 6371  # km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a =  sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = radius * c

    return d

def find_recurrences(frontier, child_node):
    for index in range(len(frontier)):
        if frontier[index][1].name == child_node.name:
            return index
    return -1

def replace_nodes(child_node, frontier, index, path_cost):
    new_tuple = (path_cost, child_node)
    frontier[index] = new_tuple

def display_result(result):
    if(result != 'Failure, cannot find the optimal path'):
        result_temp = result
        path = result_temp.name
        while result_temp.parent is not None:
            result_temp = result_temp.parent
            path = result_temp.name + ' --> ' + path
        print('\nThe shortest path is: ' + str(path) + '\nThe path cost is: ' + '{:.3f} km\n'.format(result.edges_cost))
    else:
        print('\n' + result)
