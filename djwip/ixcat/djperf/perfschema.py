import datajoint as dj

schema = dj.schema(dj.config['database.schema'], locals())

@schema
class Lab(dj.Manual): 
    definition = """ # Lab
    lab : varchar(255)  #  lab conducting the study
    ----
    institution  : varchar(255)  # Institution to which the lab belongs
    """

@schema
class Keyword(dj.Lookup):
    definition = """
    # Tag of study types
    keyword : varchar(24)  
    """
    contents = zip(['behavior', 'extracellular', 'photostim'])


@schema
class Study(dj.Manual):
    definition = """
    # Study 
    study : varchar(8)    # short name of the study
    --- 
    study_description : varchar(255)   #  
    -> Lab
    reference_atlas : varchar(255)   # e.g. "paxinos"
    """
    
@schema
class StudyKeyword(dj.Manual):
    definition = """
    # Study keyword (see general/notes)
    -> Study
    -> Keyword
    """

@schema
class Publication(dj.Manual):
    definition = """
    # Publication
    doi  : varchar(60)   # publication DOI
    ----
    full_citation : varchar(4000)
    authors='' : varchar(4000)
    title=''   : varchar(1024)
    """
    
@schema
class RelatedPublication(dj.Manual):
    definition = """
    -> Study
    -> Publication
    """



@schema
class AnimalSource(dj.Lookup):
    definition = """
    animal_source  : varchar(30) 
    """
    contents = zip(['unknown', 'JAX']) 


@schema
class Strain(dj.Lookup):
    definition = """  # Mouse strain
    strain  : varchar(30)  # mouse strain    
    """
    contents = zip(['kj18', 'kl100', 'ai32', 'pl56'])
    

@schema
class GeneModification(dj.Lookup):
    definition = """
    gene_modification : varchar(60)
    """
    contents = zip(['sim1-cre', 'rbp4-cre', 'chr2-eyfp', 'tlx-cre'])
    

@schema
class User(dj.Lookup):
    definition = """
    # User (lab member)
    username  : varchar(16) #  database username
    ----
    full_name = ''  : varchar(60)
    """

@schema
class Subject(dj.Manual):
    definition = """
    subject_id  : int   # institution animal ID  
    --- 
    species        : varchar(30)
    date_of_birth  : date   
    sex            : enum('M','F','Unknown')
    -> [nullable] AnimalSource
    """

    class GeneModification(dj.Part):
        definition = """  # Subject's gene modifications
        -> Subject
        -> GeneModification
        """

    class Strain(dj.Part):
        definition = """
        -> Subject
        -> Strain
        """


@schema
class Session(dj.Manual):
    definition = """
    -> Subject
    session  :  int 
    ---
    -> Study
    record         : int
    sample         : int
    session_date	: date		# session date
    session_suffix	: char(2)	# suffix for disambiguating sessions
    (experimenter) -> User
    session_start_time	: datetime
    """


@schema
class Ephys(dj.Imported):
    definition = """
    -> Session
    """

    class Electrode(dj.Part):
        definition = """
        -> Ephys
        electrode	: smallint	# electrode no
        ---
        electrode_x	: decimal(3,2)	# (x in mm)
        electrode_y	: decimal(3,2)	# (y in mm)
        """

    class Mapping(dj.Part):
        definition = """
        -> Ephys
        """

    class Unit(dj.Part):
        definition = """
        -> Ephys
        cell_no		: int		# cell no
        """

    class Spikes(dj.Part):
        definition = """
        -> Ephys.Unit
        ---
        spike_times	: longblob	# all events
        """


@schema
class Movie(dj.Manual):
    definition = """
    movie_id   :  smallint   # movie IDs
    ----
    x		   : int
    y		   : int
    dx		   : int
    dy		   : int
    dim_a	   : int
    dim_b		: int
    bpp		: tinyint	# bits per pixel
    pixel_size	: decimal(3,2)	# (mm)
    movie	: longblob	# 3d array
    """


@schema
class Stimulus(dj.Imported):
    definition = """
    # A stimulus session comprising multiple trials
    -> Session
    """

    class Trial(dj.Part):

        definition = """
        -> Stimulus
        trial_idx  :  smallint  # trial within 
        ---
        -> Movie
        start_time	: float    # (s)
        stop_time	: float    # (s)
        timestamps	: longblob # (s)
        """


@schema
class RF(dj.Computed):
    definition = """
    # Receptive Fields
    -> Ephys
    -> Stimulus 
    """
     
    class Unit(dj.Part):
        definition = """
        # Receptive fields
        -> RF
        -> Ephys.Spikes
        ----
        rf : longblob 
        """
