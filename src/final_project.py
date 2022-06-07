#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" Final Project """
__author__="Tho Tran"

import sys
import heapq
import helper_functions as hf

def get_cpd_parks_dict():    #returns a dictionary of parks 
    read_parks = open('CPD_Park_Art.csv', 'r').readlines()      #list of strings in this format park,x_coord,y_coord,neighbors
    cpd_parks = {}
    for l in range(len(read_parks)):
        new_line = read_parks[l].replace('\n', '')
        line_split = new_line.split(',')
        cpd_parks[line_split[0]] = line_split[1:]     #format name:[x_coord,y_coord,neighbors]
    return dict(cpd_parks)

def get_landmarks_dict():    #returns a dictionary of destinations
    read_landmarks = open('Chicago_Landmarks.csv', 'r').readlines()     #list of strings in this format name,x_coord,y_coord,neighbors
    landmarks = {}
    for l in range(len(read_landmarks)):
        new_line = read_landmarks[l].replace('\n', '')
        line_split = new_line.split(',')
        landmarks[line_split[0]] = line_split[1:]     #format name:[x_coord,y_coord,neighbors]
    return dict(landmarks)

class ParkNode:
    def __init__(self,name,long,lat,neighbors):
        self.name = name
        self.long = float(long)
        self.lat = float(lat)
        self.parent = None      #can be a str or Nonetype
        self.neighbors = neighbors      #can be a Nonetype or list type
        self.edges_cost = float(0)      #the cost of going from the source node to this node

def a_star_search(user_location, user_dest):
    parks = get_cpd_parks_dict()     #key-pair value for each park
    landmarks = get_landmarks_dict()    #get landmarks dict for the initial and final locations 
    source = landmarks[user_location]   #data belonging to key of source node
    source_node = ParkNode(user_location, source[0], source[1], source[2:])
    dest = landmarks[user_dest]     #data belonging to key of dest node
    dest_node = ParkNode(user_dest, dest[0], dest[1], None)
    frontier = []     #each index references a tuple (path_cost,node)
    explored = []       #names of places that has been explored
    heapq.heappush(frontier, (0, source_node))   #adding the source_node to frontier

    while True:
        if len(frontier) == 0:      #if destination is isolated and no path can reach it
            return 'Failure, cannot find any path'
        current_node = heapq.heappop(frontier)[1]       #aka parent node, retrieved by --> frontier[0](index 0, index 1)
        if current_node.name == dest_node.name:
            current_node.edges_cost = current_node.parent.edges_cost + hf.find_distance(current_node.parent, current_node)  #set the total cost from source_node to dest_node
            return current_node
        explored.append(current_node.name)
        for neighbor in current_node.neighbors:
            neighbor_node = ParkNode(neighbor, parks[neighbor][0], parks[neighbor][1], parks[neighbor][2:])
            neighbor_node.parent = current_node
            neighbor_node.edges_cost = hf.find_distance(current_node, neighbor_node) + current_node.edges_cost   #set the total cost from source_node to neighbor_node     
            path_cost = neighbor_node.edges_cost + hf.find_distance(neighbor_node, dest_node)
            recur_index = hf.find_recurrences(frontier, neighbor_node)      #check if there is another instance of the child_node in the frontier (-1 = false and >-1 = true)
            if neighbor_node.name not in explored and recur_index == -1 :
                heapq.heappush(frontier, (path_cost, neighbor_node))
            elif recur_index > -1 and path_cost < frontier[recur_index][0]:    #replace the other instance in frontier if its neighbor_node's path_cost is less
                hf.replace_nodes(neighbor_node, frontier, recur_index, path_cost)

def main():
    cmd_line = sys.argv[1:]
    if len(cmd_line) > 0:
        if cmd_line[0] == 'help':
            print(hf.display_help())
    else:
        print('\n' + '-'*25 + ' Welcome to Pathfinder ' + '-'*25)
        print('\nPlease enter "help" if you need further assistance or enter "start" to start the program')
        while True:
            user_input = input('> ')
            if hf.check_user_input(user_input):
                break
            print('Please enter "help" if you need further assistance or enter "start" to start the program')

        user_location = None 
        user_dest = None
        print('''\nHere is the list of landmarks for you to select the starting location and the destination''')
        print(hf.display_landmarks(get_landmarks_dict()))
        while True:
            print('Please enter the name of your starting location (you could type in all lower case letters)')
            user_location = input('> ').upper()
            print('\nPlease enter the name of your destination (you could type in all lower case letters)')
            user_dest = input('> ').upper()
            if hf.check_spelling(user_location, user_dest, get_landmarks_dict()):
                break
            else:
                print('\n' + '*'*10 + ' PLEASE CHECK YOUR SPELLING OR AVOID ADDING EXTRANEOUS WHITESPACE ' + '*'*10 + '\n')
            
        result = a_star_search(user_location, user_dest)
        hf.display_result(result)

if __name__ == '__main__':
    main()
