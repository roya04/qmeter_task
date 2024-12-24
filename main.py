import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]  
collection = db["feedback"]


pipeline = [
   
    { 
        "$unwind": "$feedback_rate" 
    },

    
    {
        "$group": {
            "_id": {
                "branch_name": "$branch.name",
                "service_name": "$feedback_rate.service.name"
            },
            "count_1": {
                "$sum": {
                    "$cond": [ { "$eq": [ "$feedback_rate.rate_option", 1 ] }, 1, 0 ]
                }
            },
            "count_2": {
                "$sum": {
                    "$cond": [ { "$eq": [ "$feedback_rate.rate_option", 2 ] }, 1, 0 ]
                }
            },
            "count_3": {
                "$sum": {
                    "$cond": [ { "$eq": [ "$feedback_rate.rate_option", 3 ] }, 1, 0 ]
                }
            },
            "count_4": {
                "$sum": {
                    "$cond": [ { "$eq": [ "$feedback_rate.rate_option", 4 ] }, 1, 0 ]
                }
            },
            "count_5": {
                "$sum": {
                    "$cond": [ { "$eq": [ "$feedback_rate.rate_option", 5 ] }, 1, 0 ]
                }
            }
        }
    },

    
    {
        "$project": {
            "_id": 0,
            "branch_name": "$_id.branch_name",
            "service_name": "$_id.service_name",
            "rate": {
                "$multiply": [
                    100, 
                    {
                        "$divide": [
                            {
                                
                                "$add": [
                                    { "$multiply": [ "$count_1", 10 ] },
                                    { "$multiply": [ "$count_2", 5 ] },
                                    { "$multiply": [ "$count_3", 0 ] },
                                    { "$multiply": [ "$count_4", -5 ] },
                                    { "$multiply": [ "$count_5", -10 ] }
                                ]
                            },
                            {
                                
                                "$multiply": [
                                    {
                                        "$add": [
                                            "$count_1",
                                            "$count_2",
                                            "$count_3",
                                            "$count_4",
                                            "$count_5"
                                        ]
                                    },
                                    10
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    },

    
    {
        "$group": {
            "_id": "$branch_name",
            "services": {
                "$push": {
                    "service_name": "$service_name",
                    "rate_value": "$rate"
                }
            }
        }
    },

   
    {
        "$project": {
            "_id": 0,
            "branch_name": "$_id",
            "services": 1
        }
    }
]

results = list(collection.aggregate(pipeline))


rows = []
for branch_obj in results:
    branch_name = branch_obj['branch_name']
    for service in branch_obj['services']:
        rows.append({
            'Branch': branch_name,
            'Service': service['service_name'],
            'Rate Calculation': service['rate_value']
        })

print(rows)