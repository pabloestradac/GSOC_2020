# Meeting Reports



**6/26 meeting (GSoC Panel call):**

- Update documentation of the `Panel_ML` class. Follow the guidelines from [Documenting classes](https://numpydoc.readthedocs.io/en/latest/format.html#documenting-classes).
- It's better to follow the current structure of `spreg `. For each user class, there is a Base class that handle the estimation. 
- For now, the current structure of the estimations will follow as [this](https://github.com/pabloestradac/GSOC2020/blob/master/docs/structure.md).
- Create a pull request for each estimation. Also, update the current [PR #41](https://github.com/pysal/spreg/pull/41).
- Try to handle the `RuntimeWarning: Method 'bounded' does not support relative tolerance in x`.



---

**6/19 meeting (GSoC group call):**

- Assess the performance of `Panel_ML` using `timeit`.
- Create `test_Panel_ML` for unit testing.
- In future meetings, each student will have to present any results from the work he has done.



---

**6/12 meeting  (GSoC Panel call):**

- Create a notebook explaining the features of the new class `Panel_ML`. 
- Use a notebook to explain the results with an example. And use another notebook to explain the detailed estimation of `Panel_ML`.
- Use `splm` of R, to compare the results with `Panel_ML`.



---

**6/05 meeting (PySAL call):**

- Brief presentation of the current state of GSoC projects.
- PySAL development discussion.



---

**5/29 meeting (GSoC group call):**

- In future GSoC group calls, each student will have a 5-min presentation.
- PRs: does not need to be polished - in a frequent and regular fashion for timely reviews.
- GSoC project progress tracking/management:
    - GitHub project board (used by the raster project): https://help.github.com/en/github/managing-your-work-on-github/about-project-boards.
    - a separate GitHub repo for work diary (used by the `esda` project): https://github.com/jeffcsauer/GSOC2020.
    - other options: GitHub issues + PRs, Trello, etc.



---

**5/22 meeting (GSoC Panel call):**

- Panel data should be structured in 2 dimensions (n*t, k).
- Pablo got accepted for a PhD program (CONGRATS!), so he will try to speedup the proposed deliverables to finish before the 1st week of August.
- Workflow: Instead of writing all functions for FE, RE and diagnostics and then unit tests and notebooks, the workflow will be structured in blocks:
    - Data handling;
    - FE + unit tests + notebooks;
    - RE + unit tests + notebooks;
    - Diagnostics+unit tests+notebooks;
- A panel branch will be created within `pysal/spreg`. Pablo will work on a fork of this branch and will submit a PR with the work done on the previous week one or two days before our weekly Friday meetings.



---

**5/15 meeting (GSoC group call):**

- Community bonding meeting.