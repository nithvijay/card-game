def gen_random_pid(db):
    generator = str(int(db.get("pid_generator_start")) + 1)
    db.set("pid_generator_start", generator)

    new_pid = f"...xxx{generator}"
    db.sadd('set_of_pids', new_pid)
    return new_pid


def clear_database(db):
    for key in db.keys():
        db.delete(key)
