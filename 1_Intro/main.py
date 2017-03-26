# Chapter 1 - Introducion

# Import libraries
from __future__ import division
from collections import Counter
from collections import defaultdict

# Finding key connectors
# ----------------------
# Identify who the "key connectors" are among data scientists.

# Data dump 1: ID number, name
# This structure is known as a dict.
users = [
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"}
]

# Date dump 2: Friendship list, represented as lists of ID pairs
friendships = [(0,1), (0,2), (1,2), (1,3), (2,3), (3,4),
              (4,5), (5,6), (5,7), (6,8), (7,8), (8,9)]

# Add a list of friends to each user
for user in users:
    user["friends"] = []
for i, j in friendships:
    users[i]["friends"].append(users[j]) # add i as a friend of j
    users[j]["friends"].append(users[i]) # add j as a friend of i
    
# Find the total number of connections
def number_of_friends(user):
    """how many friends does _user_ have?"""
    return len(user["friends"])
total_connections = sum(number_of_friends(user) for user in users)
print("total_connections: " + str(total_connections))

# Calculate average number of connections per user
num_users = len(users)
avg_connections = total_connections / num_users
print("avg_connections: " + str(avg_connections))

# Sort form "most friends" to "least friends"
# Create a list (user_id, number_of_friends)
# Known as the network metic "degree centrality"
num_friends_by_id = [(user["id"], number_of_friends(user)) 
                     for user in users]
print("before sorting: " + str(num_friends_by_id))
num_friends_by_id_sorted = sorted(num_friends_by_id, 
       key=lambda (user_id, num_friends): num_friends,
       reverse=True)
print("after sorting: " + str(num_friends_by_id_sorted))

# Find friends of friends
# For each of a user's friends, iterate over that person's friends, and
# collect all the results. This is a poorly written functions since it
# provides every connection.
def friends_of_friend_ids_bad(user):
    return [foaf["id"]
           for friend in user["friends"]
           for foaf in friend["friends"]]
def not_the_same(user, other_user):
    """two users are not the same if they have different ids"""
    return user["id"] != other_user["id"]
def not_friends(user, other_user):
    """other_user is not a friend if he's not in user["friends"];
    that is, if he's not_the_same as all the people in user["friends]"""
    return all(not_the_same(friend, other_user) for friend in user["friends"])
def friends_of_friend_ids(user):
    return Counter(foaf["id"]
                  for friend in user["friends"]
                  for foaf in friend["friends"]
                  if not_the_same(user, foaf)
                  and not_friends(user, foaf))
print friends_of_friend_ids(users[3])

# List of data scientists' interests
interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

# Simple function that finds users with certain interests
def data_scientists_who_like(target_interest):
    return [user_id
           for user_id, user_interest in interests
           if user_interest == target_interest]

# Simple function above works but is inefficient. It is better to
# build an index from interests to users. Keys are interests, values 
# are lists of user_ids with that interest.
user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)
    
# And another index from users to interests.
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)
    
# Find who has the most interest in common with a given user.
def most_common_interest_with(user):
    return Counter(interested_user_id
                  for interest in interests_by_user_id[user["id"]]
                  for interested_user_id in user_ids_by_interest[interest]
                  if interested_user_id != user["id"])
print(most_common_interest_with(users[3]))

# List of data scientis salaries based on tenure
salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
                        (48000, 0.7), (76000, 6),
                        (69000, 6.5), (76000, 7.5),
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]

# Average salary of each tenure
# Keys are years, values are lists of the salaries for each tenure
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)
# Keys are years, each value is average salary for that tenure
# Note that since none of the users have the same tenure, it just reports 
# each individidual's salary.
average_salary_by_tenure = {
    tenure : sum(salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

# Instead we want to bucket the tenures.
def tenure_bucket(tenure):
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"

# Group salaries in each bucket
# Keys are tenure buckets, values are lists of salaries for that bucket
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

# Compute average salary for each group.
# Keys are tenure buckets, values are average salary for that bucket
average_salary_by_bucket = {
    tenure_bucket : sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.iteritems()
}
print(average_salary_by_bucket)