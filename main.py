import random

import numpy as np
import pandas as pd


class BankSimulation:
    def __init__(self):
        self.clock = 0.0  
        self.num_arrivals = 0  
        self.t_arrival = self.gen_int_arr()  
        self.t_departure1 = float('inf')  
        self.t_departure2 = float('inf')  
        self.dep_sum1 = 0  
        self.dep_sum2 = 0  
        self.state_T1 = 0  
        self.state_T2 = 0  
        self.total_wait_time = 0.0  
        self.num_in_q = 0  
        self.number_in_queue = 0  
        self.num_in_system = 0  
        self.num_of_departures1 = 0  
        self.num_of_departures2 = 0  
        self.lost_customers = 0  

    def time_adv(self):  
        t_next_event = min(self.t_arrival, self.t_departure1, self.t_departure2)  
        self.total_wait_time += (self.num_in_q * (t_next_event - self.clock))
        self.clock = t_next_event

        if self.t_arrival < self.t_departure1 and self.t_arrival < self.t_departure2:
            self.arrival()
        elif self.t_departure1 < self.t_arrival and self.t_departure1 < self.t_departure2:
            self.teller1()
        else:
            self.teller2()

    def arrival(self):
        self.num_arrivals += 1
        self.num_in_system += 1

        if self.num_in_q == 0:  
            if self.state_T1 == 1 and self.state_T2 == 1:
                self.num_in_q += 1
                self.number_in_queue += 1
                self.t_arrival = self.clock + self.gen_int_arr()


            elif self.state_T1 == 0 and self.state_T2 == 0:

                if np.random.choice([0, 1]) == 1:
                    self.state_T1 = 1
                    self.dep1 = self.gen_service_time_teller1()
                    self.dep_sum1 += self.dep1
                    self.t_departure1 = self.clock + self.dep1
                    self.t_arrival = self.clock + self.gen_int_arr()

                else:
                    self.state_T2 = 1
                    self.dep2 = self.gen_service_time_teller2()
                    self.dep_sum2 += self.dep2
                    self.t_departure2 = self.clock + self.dep2
                    self.t_arrival = self.clock + self.gen_int_arr()


            elif self.state_T1 == 0 and self.state_T2 == 1:  
                self.dep1 = self.gen_service_time_teller1()
                self.dep_sum1 += self.dep1
                self.t_departure1 = self.clock + self.dep1
                self.t_arrival = self.clock + self.gen_int_arr()
                self.state_T1 = 1
            else:  
                self.dep2 = self.gen_service_time_teller2()
                self.dep_sum2 += self.dep2
                self.t_departure2 = self.clock + self.dep2
                self.t_arrival = self.clock + self.gen_int_arr()
                self.state_T2 = 1

        elif self.num_in_q < 4 and self.num_in_q >= 1:
            self.num_in_q += 1
            self.number_in_queue += 1  
            self.t_arrival = self.clock + self.gen_int_arr()

        elif self.num_in_q == 4:  
            if np.random.choice([0, 1]) == 0:
                self.num_in_q += 1
                self.number_in_queue += 1
                self.t_arrival = self.clock + self.gen_int_arr()
            else:
                self.lost_customers += 1


        elif self.num_in_q >= 5:  
            if np.random.choice([0, 1], p=[0.4, 0.6]) == 0:
                self.t_arrival = self.clock + self.gen_int_arr()
                self.num_in_q += 1
                self.number_in_queue += 1
            else:
                self.lost_customers += 1

    def teller1(self):  
        self.num_of_departures1 += 1
        self.num_in_system -= 1
        if self.num_in_q > 0:
            self.dep1 = self.gen_service_time_teller1()
            self.dep_sum1 += self.dep1
            self.t_departure1 = self.clock + self.dep1
            self.num_in_q -= 1
        else:
            self.t_departure1 = float('inf')
            self.state_T1 = 0

    def teller2(self):  
        self.num_of_departures2 += 1
        self.num_in_system -= 1
        if self.num_in_q > 0:
            self.dep2 = self.gen_service_time_teller2()
            self.dep_sum2 += self.dep2
            self.t_departure2 = self.clock + self.dep2
            self.num_in_q -= 1
        else:
            self.t_departure2 = float('inf')
            self.state_T2 = 0

    def gen_int_arr(self):
        ehsan = (-np.log(1 - (np.random.uniform(low=0.0, high=1.0))) * 3)
        print(ehsan)
        return ehsan

    def gen_service_time_teller1(self):
        return (-np.log(1 - (np.random.uniform(low=0.0, high=1.0))) * 1.2)

    def gen_service_time_teller2(self):
        return (-np.log(1 - (np.random.uniform(low=0.0, high=1.0))) * 1.5)


s = BankSimulation()
df = pd.DataFrame(columns=['Average interarrival time', 'Average service time teller1', 'Average service time teller 2',
                           'Utilization teller 1', 'Utilization teller 2', 'People who had to wait in line',
                           'Total average wait time', 'Lost Customers'])
temp_list = []
for i in range(100):
    np.random.seed(random.randint(1,100))
    s.__init__()
    while s.clock <= 240:
        s.time_adv()
    a = pd.Series([s.clock / s.num_arrivals, s.dep_sum1 / s.num_of_departures1, s.dep_sum2 / s.num_of_departures2,
                   s.dep_sum1 / s.clock, s.dep_sum2 / s.clock, s.number_in_queue, s.total_wait_time, s.lost_customers],
                  index=df.columns)

    temp_list.append(a)
    df = pd.DataFrame.from_records(temp_list)

df.to_csv('results.csv')
df.to_excel('results.xlsx')
