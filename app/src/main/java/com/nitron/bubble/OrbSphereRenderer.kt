package com.nitron.bubble

import android.graphics.Bitmap
import android.opengl.GLES20
import android.opengl.GLSurfaceView
import android.opengl.GLUtils
import android.opengl.Matrix
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.FloatBuffer
import java.nio.ShortBuffer
import javax.microedition.khronos.egl.EGLConfig
import javax.microedition.khronos.opengles.GL10
import kotlin.math.cos
import kotlin.math.sin

class OrbSphereRenderer : GLSurfaceView.Renderer {

    @Volatile var rotationX = 0f
    @Volatile var rotationY = 0f
    @Volatile var zoom = 1f
    @Volatile var pendingTextureBitmap: Bitmap? = null

    private var program = 0
    private var textureId = 0
    private var hasTexture = false

    private lateinit var vertexBuffer: FloatBuffer
    private lateinit var normalBuffer: FloatBuffer
    private lateinit var texCoordBuffer: FloatBuffer
    private lateinit var indexBuffer: ShortBuffer
    private var indexCount = 0

    private val projectionMatrix = FloatArray(16)
    private val viewMatrix = FloatArray(16)
    private val modelMatrix = FloatArray(16)
    private val mvMatrix = FloatArray(16)
    private val mvpMatrix = FloatArray(16)

    private val vertexShaderCode = """
        uniform mat4 uMVPMatrix;
        uniform mat4 uModelMatrix;
        attribute vec4 aPosition;
        attribute vec3 aNormal;
        attribute vec2 aTexCoord;
        varying vec3 vNormal;
        varying vec2 vTexCoord;
        void main() {
            gl_Position = uMVPMatrix * aPosition;
            vNormal = mat3(uModelMatrix[0].xyz, uModelMatrix[1].xyz, uModelMatrix[2].xyz) * aNormal;
            vTexCoord = aTexCoord;
        }
    """.trimIndent()

    private val fragmentShaderCode = """
        precision mediump float;
        uniform sampler2D uTexture;
        varying vec3 vNormal;
        varying vec2 vTexCoord;
        void main() {
            vec3 lightDir = normalize(vec3(0.4, 0.6, 1.0));
            float diff = max(dot(normalize(vNormal), lightDir), 0.0);
            float lighting = 0.35 + 0.65 * diff;
            vec4 texColor = texture2D(uTexture, vTexCoord);
            gl_FragColor = vec4(texColor.rgb * lighting, texColor.a);
        }
    """.trimIndent()

    override fun onSurfaceCreated(gl: GL10?, config: EGLConfig?) {

        GLES20.glClearColor(0f, 0f, 0f, 0f)
        GLES20.glEnable(GLES20.GL_DEPTH_TEST)
        GLES20.glEnable(GLES20.GL_BLEND)
        GLES20.glBlendFunc(GLES20.GL_SRC_ALPHA, GLES20.GL_ONE_MINUS_SRC_ALPHA)

        val vertexShader = loadShader(GLES20.GL_VERTEX_SHADER, vertexShaderCode)
        val fragmentShader = loadShader(GLES20.GL_FRAGMENT_SHADER, fragmentShaderCode)

        program = GLES20.glCreateProgram()
        GLES20.glAttachShader(program, vertexShader)
        GLES20.glAttachShader(program, fragmentShader)
        GLES20.glLinkProgram(program)

        buildSphere(1f, 32, 32)

        val textures = IntArray(1)
        GLES20.glGenTextures(1, textures, 0)
        textureId = textures[0]
    }

    override fun onSurfaceChanged(gl: GL10?, width: Int, height: Int) {
        GLES20.glViewport(0, 0, width, height)

        val aspect = width.toFloat() / height.toFloat()
        Matrix.perspectiveM(projectionMatrix, 0, 45f, aspect, 1f, 10f)

        Matrix.setLookAtM(
            viewMatrix, 0,
            0f, 0f, 3f,
            0f, 0f, 0f,
            0f, 1f, 0f
        )
    }

    override fun onDrawFrame(gl: GL10?) {

        pendingTextureBitmap?.let { bitmap ->
            uploadTexture(bitmap)
            pendingTextureBitmap = null
        }

        GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT or GLES20.GL_DEPTH_BUFFER_BIT)

        if (!hasTexture) return

        GLES20.glUseProgram(program)

        Matrix.setIdentityM(modelMatrix, 0)
        Matrix.scaleM(modelMatrix, 0, zoom, zoom, zoom)
        Matrix.rotateM(modelMatrix, 0, rotationX, 1f, 0f, 0f)
        Matrix.rotateM(modelMatrix, 0, rotationY, 0f, 1f, 0f)

        Matrix.multiplyMM(mvMatrix, 0, viewMatrix, 0, modelMatrix, 0)
        Matrix.multiplyMM(mvpMatrix, 0, projectionMatrix, 0, mvMatrix, 0)

        val positionHandle = GLES20.glGetAttribLocation(program, "aPosition")
        val normalHandle = GLES20.glGetAttribLocation(program, "aNormal")
        val texCoordHandle = GLES20.glGetAttribLocation(program, "aTexCoord")
        val mvpMatrixHandle = GLES20.glGetUniformLocation(program, "uMVPMatrix")
        val modelMatrixHandle = GLES20.glGetUniformLocation(program, "uModelMatrix")
        val textureHandle = GLES20.glGetUniformLocation(program, "uTexture")

        GLES20.glEnableVertexAttribArray(positionHandle)
        vertexBuffer.position(0)
        GLES20.glVertexAttribPointer(positionHandle, 3, GLES20.GL_FLOAT, false, 0, vertexBuffer)

        GLES20.glEnableVertexAttribArray(normalHandle)
        normalBuffer.position(0)
        GLES20.glVertexAttribPointer(normalHandle, 3, GLES20.GL_FLOAT, false, 0, normalBuffer)

        GLES20.glEnableVertexAttribArray(texCoordHandle)
        texCoordBuffer.position(0)
        GLES20.glVertexAttribPointer(texCoordHandle, 2, GLES20.GL_FLOAT, false, 0, texCoordBuffer)

        GLES20.glUniformMatrix4fv(mvpMatrixHandle, 1, false, mvpMatrix, 0)
        GLES20.glUniformMatrix4fv(modelMatrixHandle, 1, false, modelMatrix, 0)

        GLES20.glActiveTexture(GLES20.GL_TEXTURE0)
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, textureId)
        GLES20.glUniform1i(textureHandle, 0)

        indexBuffer.position(0)
        GLES20.glDrawElements(GLES20.GL_TRIANGLES, indexCount, GLES20.GL_UNSIGNED_SHORT, indexBuffer)

        GLES20.glDisableVertexAttribArray(positionHandle)
        GLES20.glDisableVertexAttribArray(normalHandle)
        GLES20.glDisableVertexAttribArray(texCoordHandle)
    }

    private fun uploadTexture(bitmap: Bitmap) {
        GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, textureId)
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MIN_FILTER, GLES20.GL_LINEAR)
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_MAG_FILTER, GLES20.GL_LINEAR)
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_S, GLES20.GL_CLAMP_TO_EDGE)
        GLES20.glTexParameteri(GLES20.GL_TEXTURE_2D, GLES20.GL_TEXTURE_WRAP_T, GLES20.GL_CLAMP_TO_EDGE)
        GLUtils.texImage2D(GLES20.GL_TEXTURE_2D, 0, bitmap, 0)
        hasTexture = true
    }

    private fun loadShader(type: Int, code: String): Int {
        val shader = GLES20.glCreateShader(type)
        GLES20.glShaderSource(shader, code)
        GLES20.glCompileShader(shader)
        return shader
    }

    private fun buildSphere(radius: Float, stacks: Int, slices: Int) {

        val vertices = mutableListOf<Float>()
        val normals = mutableListOf<Float>()
        val texCoords = mutableListOf<Float>()
        val indices = mutableListOf<Short>()

        for (i in 0..stacks) {
            val v = i.toFloat() / stacks
            val phi = v * Math.PI.toFloat()

            for (j in 0..slices) {
                val u = j.toFloat() / slices
                val theta = u * 2f * Math.PI.toFloat()

                val x = radius * sin(phi) * cos(theta)
                val y = radius * cos(phi)
                val z = radius * sin(phi) * sin(theta)

                vertices.add(x)
                vertices.add(y)
                vertices.add(z)

                normals.add(x / radius)
                normals.add(y / radius)
                normals.add(z / radius)

                texCoords.add(u)
                texCoords.add(v)
            }
        }

        for (i in 0 until stacks) {
            for (j in 0 until slices) {

                val first = i * (slices + 1) + j
                val second = first + slices + 1

                indices.add(first.toShort())
                indices.add(second.toShort())
                indices.add((first + 1).toShort())

                indices.add(second.toShort())
                indices.add((second + 1).toShort())
                indices.add((first + 1).toShort())
            }
        }

        vertexBuffer = toFloatBuffer(vertices.toFloatArray())
        normalBuffer = toFloatBuffer(normals.toFloatArray())
        texCoordBuffer = toFloatBuffer(texCoords.toFloatArray())
        indexBuffer = toShortBuffer(indices.toShortArray())
        indexCount = indices.size
    }

    private fun toFloatBuffer(data: FloatArray): FloatBuffer {
        return ByteBuffer.allocateDirect(data.size * 4)
            .order(ByteOrder.nativeOrder())
            .asFloatBuffer()
            .put(data)
            .apply { position(0) }
    }

    private fun toShortBuffer(data: ShortArray): ShortBuffer {
        return ByteBuffer.allocateDirect(data.size * 2)
            .order(ByteOrder.nativeOrder())
            .asShortBuffer()
            .put(data)
            .apply { position(0) }
    }
}
