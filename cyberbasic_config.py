# cyberbasic_config.py
# Reference: CharmingBlaze/cyberbasic Official Specification (2026)

KEYWORDS = [
    # Core Declarations & Types
    "VAR", "LET", "CONST", "DIM", "TYPE", "ENDTYPE", "AS", "ENUM", 
    "FUNCTION", "ENDFUNCTION", "RETURN", "IMPORT", "INCLUDE",
    
    # ECS & State Machine (V2 Specials)
    "ENTITY", "COMPONENT", "SYSTEM", "END", "STATE", "TRANSITION", "TO", 
    "ON", "UPDATE", "RUN", "ADD", "REMOVE", "YIELD", "AWAIT",
    
    # Control Flow
    "IF", "THEN", "ELSE", "ELSEIF", "FOR", "NEXT", "WHILE", "WEND", 
    "SELECT", "CASE", "STEP", "GOSUB", "GOTO", "REM"
]

# Primary Categories from the 527 built-in functions
FUNCTIONS = [
    # Window & Core
    "INITWINDOW", "CLOSEWINDOW", "WINDOWSHOULDCLOSE", "SETTARGETFPS",
    "GETSCREENWIDTH", "GETSCREENHEIGHT", "SETWINDOWTITLE", "DRAWFPS",
    
    # Drawing (2D/3D)
    "BEGINDRAW", "ENDDRAW", "CLEARBACKGROUND", "DRAWCIRCLE", "DRAWRECTANGLE", 
    "DRAWLINE", "DRAWTEXT", "DRAWPOLY", "DRAWTEXTURE", "DRAWMESH", 
    "DRAWMODEL", "DRAWGRID", "BEGINMODE2D", "ENDMODE2D", "BEGINMODE3D", "ENDMODE3D",
    
    # Input & Collision
    "ISKEYDOWN", "ISKEYPRESSED", "GETMOUSEPOSITION", "ISMOUSEBUTTONDOWN",
    "CHECKCOLLISIONRECS", "CHECKCOLLISIONCIRCLES", "GETGAMEPADAXISVALUE",
    
    # Audio & Physics
    "INITAUDIO", "PLAYSOUND", "LOADMUSIC", "UPDATEMUSIC", "INITPHYSICS",
    "UPDATEPHYSICS", "CREATEBODY", "ADDFORCE", "GETBODYPOSITION"
]

# Standard Raylib Color Constants (often used as keywords in CB2)
COLORS = {
    "bg": "#1e1e1e", "fg": "#ffffff", "keyword": "#569cd6",
    "function": "#dcdcaa", "comment": "#6a9955", "string": "#ce9178"
}

# Official Color Themes
THEMES = {
    "Dracula": {
        "bg": "#282a36",
        "fg": "#f8f8f2",
        "keyword": "#ff79c6",
        "function": "#50fa7b",
        "comment": "#6272a4",
        "string": "#f1fa8c",
        "header": "#21222c",

        "current_line": "#343746",
        "current_word": "#44475a",
        "match_bracket": "#6272a4"
    },

    "Classic Dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "keyword": "#569cd6",
        "function": "#dcdcaa",
        "comment": "#6a9955",
        "string": "#ce9178",
        "header": "#2d2d2d",

        "current_line": "#2a2d2e",
        "current_word": "#3a3d3e",
        "match_bracket": "#505050"
    }
}

# Current Font Settings
FONT_FAMILY = "Consolas"
FONT_SIZE = 12

# (Existing KEYWORDS and FUNCTIONS lists remain here...)
