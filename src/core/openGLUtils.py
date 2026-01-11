from OpenGL.GL import *

class OpenGLUtils(object):
    @staticmethod
    def printSystemInfo():
        # Get system information
        print(f"  Vendor: {glGetString(GL_VENDOR).decode("utf-8")}")
        print(f"Renderer: {glGetString(GL_RENDERER).decode("utf-8")}")
        print(f"OpenGL version supported: {glGetString(GL_VERSION).decode("utf-8")}")
        print(f"  GLSL version supported: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode("utf-8")}")

    @staticmethod
    def initialiseShader(shaderCode, shaderType):
        # Set shader version
        shaderCode = "#version 330\n" + shaderCode

        # Initialise shader
        shaderRef = glCreateShader(shaderType)
        glShaderSource(shaderRef, shaderCode)
        glCompileShader(shaderRef)

        # Error checking
        compileSuccess = glGetShaderiv(shaderRef, GL_COMPILE_STATUS)
        if not compileSuccess:
            # Fetch error message
            errorMessage = glGetShaderInfoLog(shaderRef)
            errorMessage = "\n" + errorMessage.decode("utf-8")
            
            # Free shader
            glDeleteShader(shaderRef)

            raise Exception(errorMessage)
        
        return shaderRef

    @staticmethod
    def initialiseProgram(vertexShaderCode, fragmentShaderCode):
        # Initialise shaders
        vertexShaderRef = OpenGLUtils.initialiseShader(vertexShaderCode, GL_VERTEX_SHADER)
        fragmentShaderRef = OpenGLUtils.initialiseShader(fragmentShaderCode, GL_FRAGMENT_SHADER)

        # Initialise program
        programRef = glCreateProgram()
        glAttachShader(programRef, vertexShaderRef)
        glAttachShader(programRef, fragmentShaderRef)
        glLinkProgram(programRef)

        # Error checking
        linkSuccess = glGetProgramiv(programRef, GL_LINK_STATUS)
        if not linkSuccess:
            # Fetch error message
            errorMessage = glGetProgramInfoLog(programRef)
            errorMessage = "\n" + errorMessage.decode("utf-8")
            
            # Free program
            glDeleteProgram(programRef)

            raise Exception(errorMessage)
        
        return programRef