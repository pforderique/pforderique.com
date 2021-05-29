
featured_projects = []

size = len(featured_projects)
tupled_projects = []
for idx in range(0, size, 2):
    p1 = featured_projects[idx]
    if idx + 1 < size: p2 = featured_projects[idx+1]
    else: p2 = ""

    tupled_projects.append((p1,p2))

print(tupled_projects)