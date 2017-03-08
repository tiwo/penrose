# vim : set ai et ts=4
from math import pi
import cmath # We're using complex numbers for our points on the plane
from .compat import Enum

golden_ratio = .5 * (5**.5 + 1)
golden_ratio_inv = .5 * (5**.5 - 1)

#: one-tenth of the full circle
tenths = .1 * 2 * pi

class TriangleType(Enum):
    """enumerates the two types of triangles used in the Penrose tiling
    
    nb. "acute" and "obtuse" aren't for general triangles, but for those
    with angles of 32° and 72° used in the tiling
    """
    acute = 1
    obtuse = 2

# see http://preshing.com/20110831/penrose-tiling-explained/

def subdivide(triangles):
    """subdivide acute and obtuse triangles according to the rule
    """
    for triangletype, A, B, C in triangles:
        if triangletype == TriangleType.acute:
            J = B + golden_ratio_inv * (A - B)
            yield (TriangleType.acute, J, C, A)
            yield (TriangleType.obtuse, C, J, B)
        elif triangletype == TriangleType.obtuse:
            K = A + golden_ratio_inv * (B - A)
            L = A + golden_ratio_inv * (C - A)
            yield (TriangleType.obtuse, L, K, A)
            yield (TriangleType.acute, K, L, B)
            yield (TriangleType.obtuse, C, L, B)
        else:
            raise RuntimeError('not going to subdivide anything but obtuse'
                               'and acute triangles, sorry')


def dot(x, y):
    """dot product of two points
    
    Remember that we use complex numbers::
            
        >>> a, b, c= complex(1, 0), complex(20, 30), complex(4, 4)
        >>> dot(a, b)
        20.0
        >>> dot(b, c)
        200.0
        >>> dot(a, c)
        4.0
    """
    return x.real * y.real + x.imag * y.imag


def norm_sq(point):
    """
    Example::
        >>> x, y = complex(-10, 1), -4.0
        >>> norm_sq(x)
        101.0
        >>> norm_sq(y)
        16.0
    
    norm_sq is numerically just the absolute value, squared::
        >>> import math
        >>> assert math.isclose(abs(x)**2, norm_sq(x))
        
    norm_sq is numerically equal to the dot product "square":
        >>> assert math.isclose(norm_sq(x), dot(x, x))
    """
    return point.real ** 2 + point.imag ** 2


def point_segment_distance_sq(point, seg1, seg2):
    seglen_sq = norm_sq(seg1 - seg2)

    if (seglen_sq == 0.0):
        return norm_sq(point - seg1)

    # now we won't get an exception in dividing
    t = dot(point-seg1, seg2-seg1) / seglen_sq
    if t <= 0: t=0
    elif t >= 1: t=1
    # in particular, t isn't +inf or -inf anymore :-)
    return norm_sq(point - seg1 + t * (seg2 - seg1))


def _distance_at_least(P, A, B, C):
    """Give a lower bound to the distance between P and the triangle A, B, C
    
    The exact distance must be at least abs(K) - s/2, where K is one of A, B,
    or C, and s is the length of a triangle edge adjacent to K.
    """

    A, B, C = A-P, B-P, C-P # move P to the origin

    mindist = float('Inf')
    for K, L in ((A, B), (B, C), (C, A)):
        side_length = abs(K - L)
        mindist = min(mindist, abs(K) - .5 * side_length,
                        abs(L) - .5 * side_length)

    return mindist


def distfilter(center, radius):
    """return True for triangles that could overlap with the given disk

    but may return True for triangles that don't (but are not too far).
    """

    def _distfilter(triangle):
        triangletype, A, B, C = triangle
        return _distance_at_least(center, A, B, C) <= radius

    return _distfilter


def _B(k):
    #return cmath.rect(1, .5*pi + (2*k+1)*tenths)
    return cmath.rect(1, (2*k+1)*tenths)

def _C(k):
    return _B(k) + _B(k-1)


def initial_star():

    triangles = []
    for k in range(5):
        triangles.append((TriangleType.obtuse, 0, _B(k), _C(k)))
        triangles.append((TriangleType.obtuse, 0, _B(k-1), _C(k)))

    return triangles


def sort_triangle_types(triangles):
    """sort the triangles into three lists, by type
    
    Example::
        
        >>> j = complex(0, 1)
        >>> tri1 = (TriangleType.obtuse, 0, 1, j)
        >>> tri2 = (TriangleType.acute, 0, -1, j)
        >>> tri3 = ('something strange', 0, -1, -1-j)
        >>> triangles = [tri1, tri2, tri3]
        >>> acute, obtuse, other = sort_triangle_types(triangles)
        >>> assert acute == [tri2]
        >>> assert obtuse == [tri1]
        >>> assert other == [tri3]
    """
    acute_triangles = []
    obtuse_triangles = []
    other_triangles = []
    for T, A, B, C in triangles:
        if T == TriangleType.acute:
            acute_triangles.append((T, A, B, C))
        elif T == TriangleType.obtuse:
            obtuse_triangles.append((T, A, B, C))
        else:
            other_triangles.append((T, A, B, C))
    return acute_triangles, obtuse_triangles, other_triangles

def _test():
    output = ['%!PS-Adobe-1.0',
              '%%BoundingBox: 0 0 1000 1000',
              '%%Pages: 1',
              '%%EndComments',
              '%%Page: 1 1',
              'gsave 1 setlinejoin 1 setlinecap .2 setlinewidth 0 setgray']
    rose = initial_star()
    for _ in range(4):
        rose = subdivide(rose)
        rose = filter(distfilter(0, 1.0), rose)
    translate = complex(500, 500)
    scale = 200

    rose = list(rose)  # don't consume the triangles; we need two passes
                       # (one fill, one stroke)

    acute_triangles,obtuse_triangles,other_triangles = sort_triangle_types(rose)

    output.append('%% %s acute, %s obtuse, %s other triangles' % (
            len(obtuse_triangles), len(acute_triangles), len(other_triangles)))

    for color, triangles in [('.8 .8 1', obtuse_triangles),
                             ('.9 1 .5', acute_triangles),
                             ('0 .5 0', other_triangles)
                             ]:
        output.append('gsave ' + color + ' setrgbcolor')
        for triangletype, A, B, C in triangles:
            A = translate + scale * A
            B = translate + scale * B
            C = translate + scale * C

            output.append('newpath %s %s moveto %s %s lineto %s %s lineto closepath fill' % (
                    A.real, A.imag, B.real, B.imag, C.real, C.imag))
        output.append('grestore')

    mark_vertex_A = 1

    for triangletype, A, B, C in rose:
        A = translate + scale * A
        B = translate + scale * B
        C = translate + scale * C
        if mark_vertex_A:
            M = A + .17*(B+C-2*A)
            N = .5*(A+M)
            output.append('%s %s moveto %s %s lineto' %
                (M.real, M.imag, N.real, N.imag))
        output.append('%s %s moveto %s %s lineto %s %s lineto' %
                (A.real, A.imag, B.real, B.imag, C.real, C.imag))

    output.extend([
                   'stroke',
                   'grestore showpage',
                   ])

    return '\n'.join(output)

if __name__ == '__main__':
    print(_test())
