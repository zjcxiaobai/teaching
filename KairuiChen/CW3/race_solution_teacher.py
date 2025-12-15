"""
This is a stub for the COMP16321 Coding Challenge.
Do not edit or delete any lines given in this file that are marked with a "(s)".
(you can move them to different lines as long as you do not change the overall structure)

Place your code below the comments marked "#Your code here".

Each method is documented to explain what work is to be placed within it.

NOTE: You can create as many more methods as you need. However, you need to add 
self as a parameter of the new method and to call it with the prefix self.name 

EXAMPLE:

def individual_race_result(self, results_string, drivers_string, race_number):#(s)
    results_string = "1, 2, 3, 4, 5"
    single_digit = self.remove_highest_value(results_string)
    return(single_digit)

def remove_highest_value(self, results_string):
    results_string.pop(10)
    return results_string
"""


class Races:#(s)

    # since the input is a long string of results and drivers, we need to separrate the information first
    # separate list
    def partition_lap_time(self, time_list):
        '''
        Docstring for partition_lap_time
        
        this function read the lap times, return a list of lap times, or crashed/retired
        '''
        inside_data = time_list.strip()[1:-1].strip() # remove the brackets and spaces
        results = []
        for item in inside_data.split(','):
            item = item.strip()
            if item == 'crashed' or item == 'retired':
                results.append(item)
            else:
                results.append(float(item))
        return results

    # separate results
    def partition_results(self, results_string):
        '''
        Docstring for partition_results
        
        This function to separate the information of results.txt, 
        race_id, driver_id, lap_times, status

        
        '''
        results = {}
        # separate lines:
        lines = results_string.strip().splitlines() # remove the space with strip, and split the lines
        for line in lines:                          # now analyze each line
            parts = line.split(',', 2)              # split the info by comma, and we know results.txt has 3 parts, race_id, driver_id and lap_times
            race_id = int(parts[0].strip())             # convert to integer
            driver_id = int(parts[1].strip())
            laps_time = parts[2].strip()
        
            # now deal with the information within laps_time
            laps_list = self.partition_lap_time(laps_time)
            laps = []
            status = 'finished'
            fail_lap = None
            for i in range(len(laps_list)):
                if laps_list[i] == 'crashed' or laps_list[i] == 'retired':
                    status = laps_list[i]
                    fail_lap = i + 1  # lap number starts from 1
                    break
                else:
                    laps.append(float(laps_list[i]))

            total_time = sum(laps)
            # save the data
            results.setdefault(race_id, {})
            results[race_id][driver_id] = {
                "laps": laps,
                "status": status,
                "fail_lap": fail_lap,
                "total_time": total_time,
            }
        return results
    # separate driver information
    def partition_drivers(self, drivers_string):
        '''
        Docstring for partition_drivers
        
        This function to separate the information of drivers.txt, 
        driver_id, driver_name, driver_team
        '''
        drivers = {}
        lines = drivers_string.strip().splitlines() # remove the space with strip, and split the lines
        for line in lines:                          # now analyze each line
            parts = line.split(',', 2)              # split the info by comma, and we know drivers.txt has 3 parts, driver_id and driver_name and driver_team
            driver_id = int(parts[0].strip())       # convert to integer
            driver_name = parts[1].strip()
            driver_team = parts[2].strip()
            drivers[driver_id] = {
                "driver_name": driver_name,
                "driver_team": driver_team
                }
        return drivers
    # helper function for suffix
    def suffix_help(self, n):
        if n > 3 and n < 21:
            return 'th'
        else:
            suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
            return suffixes.get(n % 10, 'th')

    def read_results(self):#(s)
        """
            Task 1:
            Read the contents of the text file results.txt and return it as a single string.

            Returns: 
                str: The content of the text file as a single string
        """
        with open("results.txt", 'r') as file:
            data = file.read()
            return data


    def read_drivers(self):#(s)
        """
            Task 2:
            Read the contents of the text file drivers.txt and return it as a single string.

            Returns: 
                str: The content of the text file as a single string
        """
        with open("drivers.txt", 'r') as file:
            data = file.read()
            return data

    def individual_race_result(self, results_string, drivers_string, race_number):#(s)
        """
            Task 3:
            Calculate and Output the results of a specified race. Where the race to be outputted is given by the automarker.
            This method determines the results of a specific race which is denoted by the "race_number" parameter. The winner is the driver with the lowest overall time for completing the race.
            If a driver crashes or retires their position will be determined by which lap this happens on.
        
            Parameters:
                results_string (str): The text string from Task 1
                drivers_string (str): The text string from Task 2
                race_number (int): An integer denoting which race's results to be calculated

            Returns:
                str: The results from the specified race.
        """

        # rank the races
        def output_rank_races(race_id, results, drivers):
            '''
            Docstring for output_rank_races
            based on the result rank the race / drivers
            '''
            if race_id not in results:
                return f"No results for Race {race_id}"
            #  sort the race
            race_entries = results[race_id]
            items = list(race_entries.items())
            def sort_key(item):
                driver_id, data = item
                driver_name = drivers[driver_id]["driver_name"]
                status = data["status"]
                if status == "finished":
                    return (0, data["total_time"], driver_name)  # finished drivers first and sorted by total time
                if data["fail_lap"] == 1:
                    return (1, -data["fail_lap"], 0.0, driver_name)
                # else
                return (1, -data["fail_lap"], data["total_time"], driver_name)
            items.sort(key=sort_key)
            # points award
            points_table = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            # output the result
            parts = []
            position = 1
            for driver_id, data in items:
                driver_name = drivers[driver_id]["driver_name"]
                status = data["status"]
                if status == "finished" and position <= len(points_table):
                    points = points_table[position - 1]
                else:
                    points = 0
                pos_suffix = self.suffix_help(position)
                parts.append(f"{position}{pos_suffix} {driver_name} {points}pts")
                position += 1
            return f"Results from Race {race_id}: " + ", ".join(parts)
        final = output_rank_races(race_number, self.partition_results(results_string), self.partition_drivers(drivers_string))
        return final



    def driver_in_race_result(self, results_string, drivers_string, race_number, driver_number):#(s)
        """
            Task 4:
            Output the results of a specified driver for a specified race. Where the driver and race to be outputted is given by the automarker.
            This method determines the results for a certain drivers in a specific race where the driver is denoted by "driver_number" and race by the "race_number"
        
            Parameters:
                results_string (str): The text string from Task 1
                drivers_string (str): The text string from Task 2
                race_number (int): An integer denoting which race's results to use
                driver_number (int): An integer denoting which drivers details to use

            Returns:
                str: The specific drivers race result.
        """
        # get the driver and results info
        drivers = self.partition_drivers(drivers_string)
        results = self.partition_results(results_string)
        # if driver or race do not exist
        if race_number not in results:
            return "No Results Available for Race " + str(race_number)
        race_entries = results[race_number]
        if driver_number not in race_entries:
            return "No Results Available for Driver " + str(driver_number) + ", Race " + str(race_number)
        
        # for normal output:
        driver_entries = race_entries[driver_number]
        driver_name = drivers[driver_number]["driver_name"]
        team_name = drivers[driver_number]["driver_team"]
        # check the status see if the driver finished the race
        if driver_entries["status"] == "finished":
            total_time = driver_entries["total_time"]
            mins = int(total_time // 60)
            secs = int(total_time % 60)
            return "Results for Driver " + str(driver_number) + ", Race " + str(race_number) + ": " + driver_name + ", " + team_name + ", " + str(mins) + "mins " + str(secs) + "secs"
        # if crashed or retired
        status_info = driver_entries["status"].capitalize()
        return "Results for Driver " + str(driver_number) + ", Race " + str(race_number) + ": " + driver_name + ", " + team_name + ", " + status_info





    def average_lap_times(self, results_string, drivers_string, race_number, driver_number):#(s)
        """
            Task 5:
            Output the average lap time for a specified driver to 2dp in a given race where both the driver number and race number is provided.
            The race number will be from 0-x where x is the final race in the input file. For example if race number = 2 then you provide the average lap time for the second race.
            If the race number provide is 0 then you should calculate their average lap time across every race.
        
            Parameters:
                results_string (str): The text string from Task 1
                drivers_string (str): The text string from Task 2
                race_number (int): The race number for the lap times to be averaged
                driver_number (int): The driver to be considered in the calculation

            Returns:
                float: The average lap times for the specified driver
                str: The relevant message if average lap time not appropriate
        """
        # given the driver number and race number - output the average lap time
        # means we only need the results info for this task
        results = self.partition_results(results_string)
        # if race number =0, then calculate the averge time across all races
        all_laps = []
        if race_number == 0:
            for r_id in results:
                race_entries = results[r_id]
                if driver_number in race_entries:
                    laps = race_entries[driver_number]["laps"]
                    for v in laps:
                        all_laps.append(v)
        else:
            if race_number in results and driver_number in results[race_number]:
                laps = results[race_number][driver_number]["laps"]
                for v in laps:
                    all_laps.append(v)
        # if no laps recorded
        if len(all_laps) == 0:
            return "No Average Lap Time Available"
        # now calculate the average lap time
        total_time = sum(all_laps)
        avg = total_time / len(all_laps)
        return round(avg, 2) # keep two decimal places



    def overall_table(self, results_string, drivers_string):#(s)
        """
            Task 5:
            Output the overall results table for all races.
            This is calculated by adding the points scored for each driver and placing them in order with the largest points total coming first.
        
            Parameters:
                results_string (str): The text string from Task 1
                drivers_string (str): The text string from Task 2

            Returns:
                str: The overall results table.
        """
        # load the race and driver information first
        results = self.partition_results(results_string)
        drivers = self.partition_drivers(drivers_string)
        # get a lssit of all driver ids:
        driver_ids = list(drivers.keys())
        # get the max rank in a race
        max_rank = 1
        for i in results:
            if len(results[i]) > max_rank:
                max_rank = len(results[i])
        total_points = {}
        count_position = {} # in case some drivers have the same points
        for d in driver_ids:
            total_points[d] = 0
            count_position[d] = [0] * max_rank  # [0,0,0,0,0, ...] initialize
        # now calculate the points and position and then put them into total_points and ount_position
        # points table
        def points(position):
            points_table = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
            if position <= len(points_table):
                return points_table[position - 1]
            else:
                return 0
        # rank a single race
        def rank_key(driver_id, results_key):
            driver_name = drivers[driver_id]["driver_name"]
            status = results_key["status"]
            if status == "finished":
                return (0, results_key["total_time"], driver_name)  # finished drivers first and sorted by total time
            if results_key["fail_lap"] == 1:
                return (1, -results_key["fail_lap"], 0.0, driver_name)
            # else
            return (1, -results_key["fail_lap"], results_key["total_time"], driver_name)
        # now loop races
        for i in results:
            race_entries = results[i]
            ranked_ids = list(race_entries.keys())
            ranked_ids.sort(key=lambda driver_id: rank_key(driver_id, race_entries[driver_id]))
            # now assign points and position count
            position = 1
            for driver_id in ranked_ids:
                total_points[driver_id] += points(position)
                count_position[driver_id][position - 1] += 1
                position += 1
        # now we have total points and count position, we can rank the overall table
        def overall_sort_key(driver_id):
            driver_name = drivers[driver_id]["driver_name"] 
            k = [-total_points[driver_id]]
            for c in count_position[driver_id]:
                k.append(-c)
            k.append(driver_name)
            return tuple(k)
            
        driver_ids.sort(key=overall_sort_key)
        # output
        parts = []
        position = 1
        for driver_id in driver_ids:
            driver_name = drivers[driver_id]["driver_name"]
            driver_team = drivers[driver_id]["driver_team"]
            points_scored = total_points[driver_id]
            pos_suffix = self.suffix_help(position)
            parts.append(f"{position}{pos_suffix} {driver_name} {points_scored}pts")
            position += 1
        return "Overall Results: " + ", ".join(parts)



if __name__ == '__main__':
    import os
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent
    os.chdir(BASE_DIR)
    print("CWD is now:", os.getcwd())
    # You can place any ad-hoc testing here
    my_instance = Races()
    task_1 = my_instance.read_results()
    # print(task_1)

    task_2 = my_instance.read_drivers()
    # print(task_2)

    task_3 = my_instance.individual_race_result(task_1, task_2, 2)
    # print(task_3) 

    task_4 = my_instance.driver_in_race_result(task_1, task_2, 2, 15)
    # print(task_4)

    task_5 = my_instance.average_lap_times(task_1, task_2, 1, 15)
    # print(task_5)

    task_6 = my_instance.overall_table(task_1, task_2)
    # print(task_6)