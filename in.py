dictionary = {
    'seed' : 20,
    'mesh' : {
        'type' : 2,
        'width' : 5,
        'height' : 3,
        'n' : 3,
        'm' : 3,
        'bottomPhysical' : 1,
        'rightPhysical' : 1,
        'topPhysical' : 1,
        'leftPhysical': 1
    },
    'lines' : [
        {
            'count' : 1,
            'size' : {
                'max' : 1,
                'min' : 0.4
            },
            'physical' : 7
        },
        {
            'count' : 4,
            'size' : {
                'max' : 3,
                'min' : 2.4
            },
            'physical' : 8
        }
    ],
    'circles' : [
        {
            'perforated' : True,
            'physical' : 6,
            'count' : 4,
            'size' : {
                'max' : 1,
                'min' : 0.5
            },
            'area' : {
                'minx' : 1.5,
                'maxx' : 3.5,
                'miny' : 1.5,
                'maxy' : 3.5
            }
        }
    ],
    'ellipses' : [
        {
            'physical' : 7,
            'perforated' : True,
            'count' : 2,
            'sizeA' : {
                'max' : 1,
                'min' : 0.2
            },
            'sizeB' : {
                'max' : 0.5,
                'min' : 0.1
            },
            'angle' : {
                'max' : 30,
                'min' : 0
            },
            'area' : {
                'minx' : 1.5,
                'maxx' : 3.5,
                'miny' : 1.5,
                'maxy' : 3.5
            }
        }
    ]
}