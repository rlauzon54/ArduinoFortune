#!/usr/bin/env python3

import os.path

class Fortune:

    files=["art", "ascii-art", "computers", "cookie", "debian", 
           "definitions", "disclaimer", "education", "ethnic", 
           "food", "fortunes", "goedel", "humorists", "kids", 
           "law", "linux", "literature", "love", "magic", 
           "medicine", "men-women", "miscellaneous", "news",
           "paradoxum", "people", "pets", "platitudes", "politics",
           "riddles", "science", "sports", "startrek",
           "translate-me", "wisdom", "work", "zippy"]
    counts={}

    def get_counts_from_cache(self,cache_file):
        with open(cache_file) as file:
            for line in file:
                parts=line.strip().split(" ")
                self.counts[parts[0]] = int(parts[1])


    def create_count_cache(self,cache_file):
        with open(cache_file,"w") as file:
            for name in self.files:
                count=self.get_fortune_count(name)
                file.write("{} {}\n".format(name,count))
                self.counts[name] = count


    def cache_fortune_counts(self):
        cache_file="count_cache"

        if os.path.exists(cache_file):
            self.get_counts_from_cache(cache_file)
        else:
            self.create_count_cache(cache_file)


    def get_fortune_count(self,fortune_file):
        fortune_count=0

        with open(fortune_file) as file:
            for line in file:
                if line[0:1] == "%":
                    fortune_count = fortune_count +1

        return(fortune_count)


    def get_fortune_text(self,fortune_file, fortune_num):
        fortune_count=0
        fortune=[]

        with open(fortune_file) as file:
            for line in file:
                if line[0:1] == "%":
                    fortune_count = fortune_count +1
                    if len(fortune) > 0:
                        return fortune

                if fortune_count == fortune_num:
                    if line[0:1] != "%":
                        fortune.append(line.rstrip())

        return("Error finding fortune")


    def get_fortune(self, fortune_file,fortune_num):
        return(self.get_fortune_text(fortune_file,fortune_num))
