'''
Created on Feb 14, 2016

@author: physicalattraction
'''

from datetime import datetime


class TinderUser(object):

    def __init__(self, data_dict):
        self.d = data_dict

    @property
    def id(self):
        return self.d['_id']

    @property
    def ago(self):
        raw = self.d.get('ping_time')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            secs_ago = int(datetime.now().strftime("%s")) - int(d.strftime("%s"))
            if secs_ago > 86400:
                return u'{days} days ago'.format(days=secs_ago / 86400)
            elif secs_ago < 3600:
                return u'{mins} mins ago'.format(mins=secs_ago / 60)
            else:
                return u'{hours} hours ago'.format(hours=secs_ago / 3600)

        return '[unknown]'

    @property
    def bio(self):
        '''Return a representation of the user's bio'''
        return self.d.get('bio')

    @property
    def name(self):
        '''Return the user name'''
        return self.d.get('name')

    @property
    def age(self):
        '''Return the user age in years'''

        raw = self.d.get('birth_date')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            return datetime.now().year - int(d.strftime('%Y'))

        return 0

    @property
    def jobs(self):
        '''Return a list of jobs. Format per element: "title - company"'''
        jobs = list()
        if 'jobs' in self.d:
            for job in self.d.get('jobs'):
                this_job = list()
                if 'title' in job and 'name' in job['title']:
                    this_job.append(job['title']['name'])
                if 'company' in job and 'name' in job['company']:
                    this_job.append(job['company']['name'])
                if len(this_job) > 0:
                    this_job_string = ' - '.join(this_job)
                    jobs.append(this_job_string)
        return jobs

    @property
    def schools(self):
        '''Return a list of schools. Each school is a dictionary with id and name.'''
        if 'schools' in self.d:
            return self.d.get('schools')

    @property
    def school_names(self):
        '''Return a list of school names.'''
        return [school.get('name') for school in self.schools]

    @property
    def common_friends(self):
        '''Return a list of common friends. Format per element: "name"'''
        common_friends = list()
        for friend in common_friends:
            print(friend)
            common_friends.append(friend['name'])
        return common_friends

    @property
    def distance(self):
        '''Return the distance in km. Format: integer'''
        distance_in_km = int(round(self.d['distance_mi'] * 1.609))
        return distance_in_km

    def __unicode__(self):
        return u'{name} ({age}), {distance} km, {ago}'.format(
            name=self.d['name'],
            age=self.age,
            distance=self.distance,
            ago=self.ago
        )
