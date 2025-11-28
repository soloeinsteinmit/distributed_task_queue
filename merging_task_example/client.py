from celery import group, chord

from worker import movie_info_a, movie_info_b, movie_info_c, combine_parts

prompt = 'Tell me about the movie Shutter Island.'

# CHORD PATTERN: Parallel tasks + Callback
# A chord combines a group of parallel tasks with a callback that runs after all complete.

# Step 1: Create a group of parallel tasks
# All three movie_info_* tasks will execute simultaneously in separate workers
# .s() creates a task signature (task definition without executing it yet)
header = group(
    movie_info_a.s(prompt),      # Worker 1: Gets movie info from source A
    movie_info_b.s(prompt),      # Worker 2: Gets movie info from source B
    movie_info_c.s(prompt)       # Worker 3: Gets movie info from source C
)

# Step 2: Define the chord with callback
# chord(header)(callback) means:
#   - Run all tasks in 'header' in parallel
#   - When ALL complete, call combine_parts with their results as arguments
#   - combine_parts receives: [result_a, result_b, result_c]
result = chord(header)(combine_parts.s())

# Step 3: Block and wait for the entire workflow to finish
# .get() is a blocking call that waits for the chord to complete
combined = result.get()

print(combined)
