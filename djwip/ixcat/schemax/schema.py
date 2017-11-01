
import datajoint as dj

schema = dj.schema('tutorial_schemax', locals())


@schema
class Animal(dj.Manual):
    definition = '''
    animal_id:		int		# animal id
    ---
    animal_name:	varchar(20)	# animal name
    animal_desc:	varchar(255)	# animal desc
    '''


@schema
class Session(dj.Manual):
    definition = '''
    -> Animal
    session_id:		int		# session id
    ---
    session_date:	date		# session date
    '''


@schema
class TrialType(dj.Lookup):
    definition = '''
    trial_type:		varchar(16)	# trial type
    '''
    contents = zip(['fun', 'games', 'injury'])


@schema
class SomeMeasurement(dj.Manual):
    # test for decimal fields
    definition = '''
    -> Animal
    measurement_id:     int             # measurement id
    ---
    value:              decimal(3,2)    # measurement value
    '''


@schema
class Trial(dj.Manual):
    definition = '''
    -> Session
    trial_id:		int		# trial id
    ---
    -> TrialType
    -> SomeMeasurement
    trial_result:	bool		# trial result
    '''
