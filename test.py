import time

# Start measuring time
start_time = time.process_time()

# Your code to be timed goes here

# Stop measuring time
end_time = time.process_time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print or use the elapsed time as needed
print(f"Elapsed time: {elapsed_time} seconds")