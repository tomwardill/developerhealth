from pymongo import Connection


class HRM:
    def __init__( self, agentConfig, mainLogger, rawConfig ):
        self.agentConfig = agentConfig
        self.mainLogger = mainLogger
        self.rawConfig = rawConfig
    
    def run(self):
        connection = Connection()
        db = connection.developerhealth
        recent_hrm = db.hrm.find().sort('time', -1).limit(1).next()
        data = {}
        data['hrm'] = recent_hrm['value']
        return data
