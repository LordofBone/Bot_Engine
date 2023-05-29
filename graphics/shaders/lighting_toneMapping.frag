varying vec3 normal;
varying vec3 vertex;
uniform samplerCube cubeMap;

vec3 ReinhardToneMapping(vec3 color)
{
    return color / (color + vec3(1.0));
}

vec3 sRGBToLinear(vec3 color)
{
    return pow(color, vec3(2.2));
}

vec3 linearTosRGB(vec3 color)
{
    return pow(color, vec3(1.0 / 2.2));
}

void main()
{
    vec3 light_position = vec3(gl_LightSource[0].position);
    vec3 light_vector = normalize(light_position - vertex);
    vec3 normal_vector = normalize(normal);
    vec3 reflection_vector = normalize(reflect(-light_vector, normal_vector));

    vec3 view_vector = normalize(-vertex);
    float diffuse = max(dot(normal_vector, light_vector), 0.0);
    float specular = max(dot(reflection_vector, view_vector), 0.0);
    specular = pow(specular, gl_FrontMaterial.shininess);

    vec4 material_color = gl_FrontMaterial.diffuse;
    vec3 final_color = (gl_FrontMaterial.emission + gl_FrontMaterial.ambient * gl_LightSource[0].ambient) +
                       (material_color * gl_LightSource[0].diffuse * diffuse) +
                       (gl_FrontMaterial.specular * gl_LightSource[0].specular * specular);
    final_color.rgb *= material_color.rgb;

    // Apply tone mapping
    final_color = ReinhardToneMapping(final_color);

    // Convert the final color from linear to sRGB
    final_color = linearTosRGB(final_color);

    gl_FragColor = vec4(final_color, 1.0);
}