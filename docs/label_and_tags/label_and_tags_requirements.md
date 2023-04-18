
**I want able to change UI inputing time entris in future**

**I want my label/tags in control**

Data's label/tag should be centralized in a place: both for app to consume and review

My concerns is: I don't know how to search for a type of activity.

**I want tag be flexible**

*  tag can add and remove fairly flexibly, without changing much code(one place in code)
*  tag force hiarchy will make it difficult to change in future. e.g
    *  family tag will include dinner, chat, trip, etc. or I want a separate tag for dinner.

Tag depend on how I want to view my time, may change in future.

Ignore tag not in system, rather than exception every data(better to summary all the tag in data but not supported in code)

**I want to see time spent on following**

Stable tag, or most important, will give it a "type"

Key metric

*  Sleep
*  Self Improving
*  work
*  exercise
*  sex
*  meditation
*  walk

Note:

*  Should describe what I did during that time, rather than how I feel.

**I want to see breakdown of other**

I only care important/major parts: 

no need to every time entry has a type, those can just tag it.

*  cooking
*  family
*  grocery
*  housework
*  numb
*  dispute

Aim is to figure out time spent on this part: 

*  Is spent for recreation/rest
    *  family
    *  friends
    *  self 
        *  blank(beach, DAI, nothing)
        *  reading for fun
*  Is spent for routine(support other activities)
    *  Do I spent too much time on things shouldn't be? i.e cooking, grocery shopping, internet.
*  Is spent on a way not enjoy life neither be productive/supportive
    *  distracted
*  Is spent on a way regretable?
    *  dispute
    *  numb
    *  pmo



**I want my time entries linked to external task tracking system**

Like Kanban board, more info provided for a unit task:

*  When start, stop
*  Parent ticket up the chain, till top-level ticket 
*  Search for any level of ticket, give me matching time entris


# Design

*  Each time entry MUST link to (leaf node)

*  selfimproving
*  exercise
*  routine
*  relax


# Task design

*  Only record issue=xx, as label
*  task tracking provider as annotation, make a detault explicit, as zenhub
*  Epic matching, convert to OneOfLabelValue matching
*  Aggregate Epic and tasks: ticket to get parent(Epic)

Note

*  Leave Epic since start to later, especially after cache system
