from nickgen.syllable_eng import SyllableEng
from nickgen.syllable_jap import SyllableJap
import os
from importlib.resources import files


class SyllableLoader:

    @staticmethod
    def LoadEng():
        # currentDir = os.path.dirname(os.path.abspath(__file__))
        # eng_path = os.path.join(currentDir, 'eng.json')
        
        eng_path = files('nickgen').joinpath('data').joinpath('eng.json')

        try:
            if not os.path.exists(eng_path):
                raise Exception(f'File not exists: {eng_path}')
            return SyllableEng.Load(eng_path)
        except:
            raise
            import sys;
            print("Unexpected error:", sys.exc_info()[0])
            raise Exception('syllableEng_0 = SyllableEng.Load')

    
    @staticmethod
    def LoadLat():
        # currentDir = os.path.dirname(os.path.abspath(__file__))
        # lat_path = os.path.join(currentDir, 'lat.json')
        
        lat_path = files('nickgen').joinpath('data').joinpath('lat.json')

        try:
            return SyllableEng.Load(lat_path)
        except:
            raise Exception('syllableEng_1 = SyllableEng.Load')


    @staticmethod
    def LoadJap():
        # currentDir = os.path.dirname(os.path.abspath(__file__))
        # jap_path = os.path.join(currentDir, 'jap.json')
        
        jap_path = files('nickgen').joinpath('data').joinpath('jap.json')
        
        try:
            return SyllableJap.Load(jap_path)
        except:
            #raise
            raise Exception('syllableJap_0 = SyllableJap.Load')