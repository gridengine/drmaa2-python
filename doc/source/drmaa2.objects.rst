.. automodule:: drmaa2

.. currentmodule:: drmaa2

Drmaa2Object
------------

.. autoclass:: drmaa2.drmaa2_object.Drmaa2Object()
    :members: to_dict
    :show-inheritance:

Version
-------

.. autoclass:: drmaa2.version.Version()
    :members: get_drmaa_version,get_drms_version,get_implementation_specific_keys,major,minor,implementation_specific
    :show-inheritance:

MachineInfo
-----------

.. autoclass:: drmaa2.machine_info.MachineInfo()
    :members: get_implementation_specific_keys,name,available,sockets,cores_per_socket,threads_per_core,load,phys_memory,virt_memory,machine_arch,machine_os_version,machine_os,implementation_specific  
    :show-inheritance:

QueueInfo
---------

.. autoclass:: drmaa2.queue_info.QueueInfo()
    :members: get_implementation_specific_keys,name,implementation_specific  
    :show-inheritance:

Job
---

.. autoclass:: drmaa2.job.Job()
    :members: id,job_name,session_name,get_info,get_state,get_template,hold,reap,release,resume,suspend,terminate,terminate_all,terminate_forced,terminate_forced_all,wait_started,wait_terminated
    :show-inheritance:

JobArray
--------

.. autoclass:: drmaa2.job_array.JobArray()
    :members: id,job_list,session_name,get_template,hold,reap,release,resume,suspend,terminate,terminate_all
    :show-inheritance:

JobInfo
-------

.. autoclass:: drmaa2.job_info.JobInfo()
    :members: get_implementation_specific_keys, __init__, allocated_machines, annotation, cpu_time, dispatch_time, exit_status, finish_time, implementation_specific, job_id, job_name, job_owner, job_state, job_sub_state, queue_name, slots, submission_machine, submission_time, terminating_signal, wallclock_time
    :show-inheritance:
    
JobTemplate
-----------

.. autoclass:: drmaa2.job_template.JobTemplate()
    :members: get_implementation_specific_keys, __init__, remote_command, args, submit_as_hold, rerunnable, job_environment, working_directory, job_category, email, email_on_started, email_on_terminated, job_name, input_path, output_path, error_path, join_files, reservation_id, queue_name, min_slots, max_slots, priority, candidate_machines, min_phys_memory, machine_os, machine_arch, start_time, deadline_time, stage_in_files, stage_out_files, resource_limits, accounting_id, implementation_specific
    :show-inheritance:

Notification
------------

.. autoclass:: drmaa2.notification.Notification()
    :members: event, session_name, job_id, job_state, implementation_specific, register_event_notification, unregister_event_notification
    :show-inheritance:

Reservation
-----------

.. autoclass:: drmaa2.reservation.Reservation()
    :members: id,session_name,get_info,get_template,terminate
    :show-inheritance:

ReservationInfo
---------------

.. autoclass:: drmaa2.reservation_info.ReservationInfo()
    :members: get_implementation_specific_keys, reservation_id, reservation_name, reserved_start_time, reserved_end_time, users_acl, reserved_slots, reserved_machines, implementation_specific  
    :show-inheritance:
    
ReservationTemplate
-------------------

.. autoclass:: drmaa2.reservation_template.ReservationTemplate()
    :members: get_implementation_specific_keys, __init__, reservation_name, start_time, end_time, duration, min_slots, max_slots, job_category, users_acl, candidate_machines, min_phys_memory, machine_os, machine_arch, implementation_specific
    :show-inheritance:

Sudo
----

.. autoclass:: drmaa2.sudo.Sudo()
    :members: __init__, username, groupname, uid, gid
    :show-inheritance:

