
from wavelet import approx_rec, baseline, denoise, enhance
from dualtree import dtanalysis, dtsynthesis, dt_approx_rec
from dtwavelets import dualtree_wavelet, qshift, ALL_QSHIFT
import matplotlib.pyplot as plt
import numpy as n
import pywt
import unittest

n.random.seed(23)

##############################################################################
###           DUAL-TREE COMPLEX WAVELET TRANSFORM
##############################################################################

class TestComplexWavelets(unittest.TestCase):

    def test_qshift(self):
        for name in ALL_QSHIFT:
            wavelets = qshift(name)

class TestDualTree(unittest.TestCase):
    
    #@unittest.expectedFailure
    def test_perfect_reconstruction_multilevel(self):
        array = n.sin(n.arange(0, 10, step = 0.01))
        coeffs = dtanalysis(data = array, level = 3)
        reconstructed = dtsynthesis(coeffs = coeffs)
        self.assertTrue(n.allclose(array, reconstructed))
    
    def test_perfect_reconstruction_max_level(self):
        array = n.sin(n.arange(0, 10, step = 0.01))
        coeffs = dtanalysis(data = array, level = 'max')
        reconstructed = dtsynthesis(coeffs = coeffs)
        self.assertTrue(n.allclose(array, reconstructed))
    
    def test_dt_approx_rec(self):
        array = n.sin(n.arange(0, 10, step = 0.01))
        test = dt_approx_rec(array = array, level = 'max', first_stage = 'bior5.5')
        self.assertTrue(array.size == test.size)


##############################################################################
###           BASELINE AND COMPANY
##############################################################################

class Test2D(unittest.TestCase):
    def setUp(self):
        self.array = n.zeros(shape = (100, 100), dtype = n.float)

class Test1D(unittest.TestCase):
    def setUp(self):
        self.array = n.zeros(shape = (100,), dtype = n.float)



class TestEdgeCases(object):

    def test_dimensions(self):
        self.assertRaises(Exception, baseline, {'data':n.zeros(shape = (3,3,3), dtype = n.uint), 'max_iter': 10, 'level': 1})

    def test_zero_level(self):
        # Since all function are based on approx_rec, we only need to test level = 0 for approx_rec
        self.assertTrue(n.allclose(self.array, approx_rec(self.array, level = 0, wavelet = 'db1')))

class TestEdgeCases1D(Test1D, TestEdgeCases): pass

class TestEdgeCases2D(Test2D, TestEdgeCases): pass



class TestTrivial(object):

    def test_baseline(self):
        self.assertTrue(n.allclose(self.array, baseline(self.array, max_iter = 10)))

    def test_denoise(self):
        self.assertTrue(n.allclose(self.array, denoise(self.array)))
    
    def test_enhance(self):
        self.assertTrue(n.allclose(self.array, enhance(self.array)))

class TestTrivial1D(Test1D, TestTrivial): pass

class TestTrivial2D(Test2D, TestTrivial): pass



class TestDenoise(object):

    def test_random(self):
        noisy = self.array + 0.05*n.random.random(size = self.array.shape)
        self.assertTrue(n.allclose(self.array, denoise( noisy, level = 'max', wavelet = 'db1' ), atol = 0.05))

class TestDenoise1D(Test1D, TestDenoise): pass

class TestDenoise2D(Test2D, TestDenoise): pass

if __name__ == '__main__':
    unittest.main()