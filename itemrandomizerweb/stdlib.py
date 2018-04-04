
# https://msdn.microsoft.com/en-us/visualfsharpdocs/conceptual/microsoft.fsharp.collections-namespace-%5bfsharp%5d
class Map:
    @staticmethod
    def toList(map):
        # returns a list of all key/value pairs in the mapping.
        # the returned list is ordered by the keys of the map.
        return [(index, map[index]) for index in sorted(map)]

class Array:
    @staticmethod
    def toList(array):
        # builds a list from the given array
        return array

    @staticmethod
    # Array.iteri (fun i _ -> swap a i (rnd.Next(i, Array.length a))) a
    def iteri(fun, array):
        # applies the given function to each element of the array.
        # the integer passed to the function indicates the index of element.
        # done in place.
        for i in range(len(array)):
            fun(i, array[i])

    @staticmethod
    def length(array):
        # returns the length of an array
        return len(array)

class List:
    @staticmethod
    def length(list):
        # gets the number of items contained in the list
        return len(list)

    @staticmethod
    def exists(fun, list):
        # tests if any element of the list satisfies the given predicate

        # take 86% off all execution time:
        #return True in [fun(elem) for elem in list]

        # do a loop and exit on first True occurence
        for elem in list:
            if fun(elem) == True:
                return True
        return False

    @staticmethod
    def filter(fun, list):
        # returns a new collection containing only the elements of the collection
        # for which the given predicate returns true
        return [elem for elem in list if fun(elem) == True]

    @staticmethod
    def find(fun, list):
        # returns the first element for which the given function returns true
        # raise: StopIteration
        return next(iter([elem for elem in list if fun(elem) == True]))

    @staticmethod
    def sortBy(fun, list):
        # sorts the given list using keys given by the given projection
        return sorted(list, key=fun)

    @staticmethod
    def append(list1, list2):
        # returns a new list that contains the elements of the first
        # list followed by elements of the second
        return list1 + list2

    @staticmethod
    def head(list):
        # returns the first element of the list
        # raise: IndexError
        return list[0]

    @staticmethod
    def toArray(list):
        return list

    @staticmethod
    def item(index, list):
        # gets the element of the list at the given position
        return list[index]

    @staticmethod
    def map(fun, list):
        # creates a new collection whose elements are the results of
        # applying the given function to each of the elements of the collection
        return [fun(elem) for elem in list]

# http://referencesource.microsoft.com/#mscorlib/system/random.cs
import time

class Random:
    # Private Constants 
    int32_maxValue = 2147483647
    int32_minValue = -2147483648
    MBIG =  int32_maxValue
    MSEED = 161803398

    # Member Variables
    inext = 0
    inextp = 0
    SeedArray = [0]*56

    def __init__(self, Seed=None):
        if Seed is None:
            Seed = int(time.time())
    
        ii = 0
        mj = 0
        mk = 0
    
        # Initialize our Seed array.
        # This algorithm comes from Numerical Recipes in C (2nd Ed.)
        subtraction = self.int32_maxValue if Seed == self.int32_minValue else abs(Seed)
        mj = self.MSEED - subtraction
        self.SeedArray[55] = mj
        mk = 1
        for i in range(1, 55):
            ii = (21*i)%55
            self.SeedArray[ii] = mk
            mk = mj - mk
            if mk < 0:
                mk += self.MBIG
            mj = self.SeedArray[ii]

        for k in range(1, 5):
            for i in range(1, 56):
                self.SeedArray[i] -= self.SeedArray[1+(i+30)%55]
                if self.SeedArray[i] < 0:
                    self.SeedArray[i] += self.MBIG

        self.inext = 0
        self.inextp = 21
        Seed = 1

    
    #/*====================================Sample====================================
    #**Action: Return a new random number [0..1) and reSeed the Seed array.
    #**Returns: A double [0..1)
    #**Arguments: None
    #**Exceptions: None
    #==============================================================================*/
    def Sample(self):
        # Including this division at the end gives us significantly improved
        # random number distribution.
        return (self.InternalSample()*(1.0/self.MBIG));

    def InternalSample(self):
        locINext = self.inext
        locINextp = self.inextp
 
        locINext += 1
        if locINext >= 56:
            locINext=1
        locINextp += 1
        if locINextp >= 56:
            locINextp = 1

        retVal = self.SeedArray[locINext]-self.SeedArray[locINextp]
 
        if retVal == self.MBIG:
            retVal -= 1
        if retVal < 0:
            retVal += self.MBIG
          
        self.SeedArray[locINext] = retVal
 
        self.inext = locINext
        self.inextp = locINextp
                    
        return retVal
    
    def GetSampleForLargeRange(self):
        # The distribution of double value returned by Sample 
        # is not distributed well enough for a large range.
        # If we use Sample for a range [self.int32_minValue..self.int32_maxValue)
        # We will end up getting even numbers only.

        result = self.InternalSample()

        # Note we can't use addition here. The distribution will be bad if we do that.
        negative = True if (self.InternalSample()%2 == 0) else False  # decide the sign based on second sample
        if negative == True:
            result = -result

        d = result
        d += (self.int32_maxValue - 1) # get a number in range [0 .. 2 * Int32MaxValue - 1)
        d /= float(2 * self.int32_maxValue - 1)

        return d

    # /*=====================================Next=====================================
    # **Returns: An int [minvalue..maxvalue)
    # **Arguments: minValue -- the least legal value for the Random number.
    # **           maxValue -- One greater than the greatest legal return value.
    # **Exceptions: None.
    # ==============================================================================*/
    def Next(self, minValue=0, maxValue=int32_maxValue):
        if minValue > maxValue:
            raise Exception("minValue > maxValue")

        range = maxValue - minValue
        if range <= self.int32_maxValue:
            retValue = ((int)(self.Sample() * range) + minValue)
        else:
            retValue = (int)((long)(self.GetSampleForLargeRange() * range) + minValue)
    
        #print("Next({}, {}) -> {}".format(minValue, maxValue, retValue))
        return retValue
    
    #/*=====================================Next=====================================
    # **Returns: A double [0..1)
    # **Arguments: None
    # **Exceptions: None
    # ==============================================================================*/
    def NextDouble(self):
        return self.Sample()
    
    #/*==================================NextBytes===================================
    # **Action:  Fills the byte array with random bytes [0..0x7f].  The entire array is filled.
    # **Returns:Void
    # **Arugments:  buffer -- the array to be filled.
    # **Exceptions: None
    # ==============================================================================*/
    def NextBytes(self, buffer):
        for i in range(0, len(buffer)):
            buffer[i] = (self.InternalSample()%(255+1))

if __name__ == "__main__":
    r = Random(42)
    print(r.Sample())
    print(r.InternalSample())
    print(r.GetSampleForLargeRange())
    print(r.Next(1000000, 9999999))
    print(r.Next())
    print(r.NextDouble())
    buffer = [0]*10
    r.NextBytes(buffer)
    print(buffer)
