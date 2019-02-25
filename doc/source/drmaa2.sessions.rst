.. automodule:: drmaa2

.. currentmodule:: drmaa2

JobSession
----------

.. autoclass:: drmaa2.job_session.JobSession()
    :members: destroy_by_name, list_session_names, __init__, name, contact, close, destroy, get_job_array, get_jobs, get_job_categories, open, run_job, run_bulk_jobs, wait_all_started, wait_all_terminated, wait_any_started, wait_any_terminated
    :show-inheritance:

MonitoringSession
-----------------

.. autoclass:: drmaa2.monitoring_session.MonitoringSession()
    :members: __init__, name, close, get_all_jobs, get_all_machines, get_all_queues, get_all_reservations, open
    :show-inheritance:

ReservationSession
------------------

.. autoclass:: drmaa2.reservation_session.ReservationSession()
    :members: destroy_by_name, list_session_names, __init__, name, contact, close, destroy, get_reservation, get_reservations, open, request_reservation
    :show-inheritance:


