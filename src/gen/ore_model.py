def ore_model(overlay, strata):
    return {
        "parent": "minecraft:block/block",
        "display": {
            "thirdperson_lefthand": {
                "rotation": [75, 45, 0],
                "translation": [0, 2.5, 0],
                "scale": [0.375, 0.375, 0.375]
            },
            "thirdperson_righthand": {
                "rotation": [75, 45, 0],
                "translation": [0, 2.5, 0],
                "scale": [0.375, 0.375, 0.375]
            }
        },
        "textures": {
            "particle": overlay
        },
        "loader": "forge:multi-layer",
        "layers": {
            "solid": {
                "parent": "minecraft:block/block",
                "textures": {
                    "base": strata
                },
                "elements": [{
                    "from": [0, 0, 0],
                    "to": [16, 16, 16],
                    "faces": {
                        "down": {
                            "texture": "#base",
                            "cullface": "down"
                        },
                        "up": {
                            "texture": "#base",
                            "cullface": "up"
                        },
                        "north": {
                            "texture": "#base",
                            "cullface": "north"
                        },
                        "south": {
                            "texture": "#base",
                            "cullface": "south"
                        },
                        "west": {
                            "texture": "#base",
                            "cullface": "west"
                        },
                        "east": {
                            "texture": "#base",
                            "cullface": "east"
                        }
                    }
                }]
            },
            "translucent": {
                "parent": "minecraft:block/block",
                "textures": {
                    "overlay": overlay
                },
                "elements": [{
                    "from": [0, 0, 0],
                    "to": [16, 16, 16],
                    "faces": {
                        "down": {
                            "texture": "#overlay",
                            "cullface": "down"
                        },
                        "up": {
                            "texture": "#overlay",
                            "cullface": "up"
                        },
                        "north": {
                            "texture": "#overlay",
                            "cullface": "north"
                        },
                        "south": {
                            "texture": "#overlay",
                            "cullface": "south"
                        },
                        "west": {
                            "texture": "#overlay",
                            "cullface": "west"
                        },
                        "east": {
                            "texture": "#overlay",
                            "cullface": "east"
                        }
                    }
                }]
            }
        }
    }
