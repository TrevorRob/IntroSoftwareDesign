Our API allows you to access data on the mean daily number of sunspots recorded per year, between the years 1771 and 1869. The following are the endpoints you can use to access/analyze the data:

```/```  - returns all of the Sunspot data [GET] to the result in the job log. 

```/year/<int:year>```  - returns the Mean Daily Sunspots recorded for your given year to the result in the job log. Make sure to input a year in the range [1771, 1869], i.e.  
```curl http://localhost:5000/year/1820```

```/max```  - returns the year that the maximum number of mean daily sunspots were recorded and the number of mean daily sunspots for that year to the result in the job log

```/min```  - returns the year that the minimum number of mean daily sunspots were recorded and the number of mean daily sunspots for that year to the result in the job log

```/plot/<string:kind>```  - creates and saves your desired plot of the data to the current directory. When the job is done, the job’s json will have a status = complete and the result will let you know that the plot has been created and the filename you can find it under. The options for the “kind” of plot are : histogram, line, and scatter. I.e.  
```curl http://localhost:5000/plot/histogram```

```/year'```  - allows you to add a new data point to the sunspot database. It takes in data in the form of a json like this:  
```{'Year': <insert new year here>, 'Mean Daily Spots: <insert mean daily spots for new year here>}```  
Here's an example of the curl statement:  
``` curl '{'Year': 2010, 'Mean Daily Spots': 17}' http://localhost:5000/year```

```/job_id/<string:jid>```  - directly returns the most current json object for the job id you input, which includes the job id, the job’s status, the job’s most current timestamp, and either the parameters and commands for the job or the result of the completed job. You can only input job id’s which you got back when you input a job (so for all endpoints before this one, you will immediately get back job id, which you can put in to this endpoint to immediately get back all of the latest information for that job id).


Because of the issue we were having with the save_job function, if you would like to run our api without going through the worker, just run ```python main2.py```. All of the endpoints are the same with the exception of the post function (which we are still working out the kinks on). An example of the post endpoint looks like this:  
```curl http://localhost:5000?year=2019&spots=20```