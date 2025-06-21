import pcg_benchmark
import PIL

if __name__ == "__main__":
    env = pcg_benchmark.make("binary-v0")
    env.seed(10)
    print("Environment created and seeded.")

    # Load data from the input file (input/input.txt)
    file_contents = ""
    with open("input/input.txt", "r") as file:
        file_contents = file.read()

    # Parse the contents by new lines and store them in a list
    file = file_contents.splitlines()
    file = [msg.strip() for msg in file if msg.strip()]

    # geberate 100 random control parameters from the control_space
    controls = [env.control_space.sample() for _ in range(100)]

    for i, line in enumerate(file):
        # replace the "],[" with a ;
        line = line.replace("],[", ";")

        # remove the "[[" and "]]" from the first and last element
        line = line.replace("[[", "").replace("]]", "")

        # parse each line int a list of list of integers
        line_as_int = [[int(num) for num in part.split(",")] for part in line.split(";")] 
        
        output = env.evaluate(line_as_int, controls[i])

        # extract the "exact values"
        quality = output[3]["quality"]
        diversity = output[3]["diversity"]
        controlability = output[3]["controlability"]
        print(f"Sample {i+1}: Quality: {quality}, Diversity: {diversity}, Controlability: {controlability}")

        # print the output
        # print(f"Sample {i+1} output: {output}")

        # save as an image
        img = env.render(line_as_int)
        img.save(f"output/sample_image{i+1}.png")

        # save the whole output as json
        with open(f"output/sample_output{i+1}.json", "w") as f:
            f.write(str(output))
            
    print("Evaluation completed.")

