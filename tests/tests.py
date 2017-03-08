import penrose
import penrose.core

def test_initial_star():
    """the star contains exactly 10 obtuse triangles"""
    
    star = penrose.initial_star()
    
    assert(len(star) == 10)
    
    obtuse = penrose.TriangleType.obtuse
    triangle_types = [T for T, A, B, C in star]
    
    assert triangle_types == 10 * [obtuse]


def test_subdivisions():
    
    ######## Test subdivisions of a 
    tri1 = penrose.initial_star()[0]
    
    assert tri1[0] == penrose.TriangleType.obtuse
    
    subtriangles = list(penrose.core.subdivide([tri1]))
    
    assert len(subtriangles) == 3
    
    acute_subtriangles, obtuse_subtriangles, other_subtriangles = (
            penrose.sort_triangle_types(subtriangles))
    
    assert len(acute_subtriangles) == 1
    assert len(obtuse_subtriangles) == 2
    assert len(other_subtriangles) == 0
    
    tri2 = acute_subtriangles[0]
    subtriangles = list(penrose.core.subdivide([tri1]))
    acute_subtriangles, obtuse_subtriangles, other_subtriangles = (
            penrose.sort_triangle_types(subtriangles))
    

if __name__ == '__main__':
    test_constants()
    test_initial_star()
    test_subdivisions()
