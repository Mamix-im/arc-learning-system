import sqlite3
import matplotlib.pyplot as plt


# Database connect
conn = sqlite3.connect("arc.db")
cur = conn.cursor()


# Data fetch
cur.execute("SELECT status FROM learning")
data = cur.fetchall()

conn.close()


done = 0
pending = 0


# Count status
for d in data:

    if d[0] == "Done":
        done += 1

    elif d[0] == "Pending":
        pending += 1


# Graph
labels = ["Done", "Pending"]
values = [done, pending]


plt.figure()
plt.bar(labels, values)
plt.title("ARC Learning Progress")
plt.xlabel("Status")
plt.ylabel("Days")

plt.show(block=False)
plt.pause(5)
plt.close()
