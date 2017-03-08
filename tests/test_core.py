import penrose.core
import math

def test_constants():
    assert math.pi == penrose.core.pi
    assert math.isclose(penrose.core.golden_ratio, 1.618033988749895)
    assert math.isclose(penrose.core.golden_ratio_inv, 0.618033988749895)
    assert math.isclose(penrose.core.golden_ratio - 1,
		    	penrose.core.golden_ratio_inv)
    assert math.isclose(1 / penrose.core.golden_ratio,
		    	penrose.core.golden_ratio_inv)
    assert math.isclose(penrose.core.golden_ratio**2 - 1,
		    	penrose.core.golden_ratio)

