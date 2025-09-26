---
title: Is Meetup Terrible or is *my* meetup terrible?
tags: [Community, Meetup, Article]
layout: post
image: /assets/images/meetup-is-terrible2.png
---

I’ve spent a lot of time and energy this year complaining about Meetup ([at the CodeBar Festival Fringe](https://hughevans.dev/meetup-is-terrible-now-codebar-festival-fringe/), [at PyCon UK](https://hughevans.dev/py-con-uk-2025/#:~:text=I%20took%20the%20opportunity%20to%20speak%20a%20bit%20about%20notanother.pizza%20and%20community%20organising%20in%20another%20%E2%80%9CMeetup%20is%20terrible%20now%E2%80%9D%20lightning%20talk.), and [on my blog](https://hughevans.dev/not-another-pizza/)). Meetup is becoming more expensive, less reliable, and generally ‘[enshittified](https://en.wikipedia.org/wiki/Enshittification)’ which came to a head at the beginning of this year when [AI Signals, a community](http://aisignals.org.uk) I organise through Meetup saw a marked drop in attendance.

The thesis of my “Meetup is Terrible Now” talk was that reducing reliance on Meetup could help with declining attendance and the burden of organising events \- rather than just speculating about this though I actually followed my own advice to see if it would work in practice.

![]({{ site.baseurl }}/assets/images/before-signals-attendance.png)

Meetup as a platform provides network effects that drive attendance, tooling for managing RSVPs and community membership, and has good SEO for discoverability via search (in part because of their capturing of the “Meetup” namespace). Any solution to my problem must still have these things to be a meaningful Meetup alternative.

Some potential solutions I proposed were:

* Moving platforms \- use another community platform like Luma, OddCircles etc instead of Meetup  
* [POSSE \- Post Own Site Syndicate Everywhere](https://indieweb.org/POSSE), maintain a central self-hosted community platform and syndicate event invites across 3rd party community platforms  
* Collaboration \- Work with other organisers to share resources and cross promote events (potentially via [notanother.pizza](http://notanother.pizza), more on this later)

Each has their own merits and issues but my hope was that in combination these three solutions might be enough to break from dependence on Meetup.

What I didn’t cover in my talk was metrics of the success of these solutions which are an important part of any initiative like this, in the end I tracked the following metrics before and after embarking on this experiment:

* Event attendance  
* Net new organisers  
* % Of event RSVPs from Meetup vs non-Meetup sources

## Putting it into practice

Working with my friend and former colleague Steve Morris, we rebranded AI Signals from AIDLE (AI and Deep Learning for Enterprise) and launched our own website. We were hugely lucky to have support from Steve ([you can read more about the strategy and brand work we did with Steve over on his blog here](https://steve-morris.medium.com/strategy-is-what-you-do-next-e39d83be3f04)) and as you’ll see this was one of the most impactful actions in this initiative, but I ran out of steam before successfully implementing POSSE for AI Signals. Starting my new role at Aiven meant I no longer had time for larger infrastructure efforts so setting up POSSE was put on hold.

We set up [a Luma calendar](https://luma.com/ai-signals?k=c&period=past) and started cross promoting events from Meetup there. We also embedded Luma as the registration system for events in our website with a view to encourage our audience to move to Luma from Meetup. 

Additionally we worked with other technical communities in London like [Women in Data](https://www.womenindata.org/) to co-host and cross promote events. 

## The result: What worked

The rebrand was enormously successful \- at the first event after the rebrand we had a turnout of 55 people, more than double the attendance of the previous event at which we only had 20 people.   
![]({{ site.baseurl }}/assets/images/after-signals-attendance.png)

This increase in attendance has been lasting \- we now see an average of 53 attendees at each event post rebrand. We also had several new organisers join, growing our team from 3 to 10 people. Anecdotally, some cited the new brand as sparking their interest in getting involved. We also saw an increase in submissions to our call for papers and three new sponsors engaging with us.

![]({{ site.baseurl }}/assets/images/ai-signals-growing-team.png)

Promoting events in parallel on Luma contributed to some net new RSVPs in this time, it’s hard to say by exactly how much though as we don’t register attendees on the door so we don’t know exactly how many people attend a given event from Meetup vs Luma. With that said though since we started promoting events on Luma 32% of our total RSVPs have been from Luma.

![]({{ site.baseurl }}/assets/images/luma-vs-meetup-post-signals.png)

[Our event in collaboration with Women in Data](https://aisignals.org.uk/events/spotlight-on-agentic-ai-women-in-data) had an above average attendance compared to other post rebrand events. I don’t have good data on referrals from cross promotion from other communities but we have seen a lot of new faces since we started collaboration with other groups. We also worked with the Civo team to promote their Civo navigate event and in exchange they helped us out with some free venue use.

## The result: What didn’t

Both our audience and audience growth remain concentrated on Meetup. We now have 4,084 members there versus only 236 on Luma. I had hoped to pull the plug on our Meetup page at the end of this year but as it stands I won’t be able to do that \- the network effects there remain too strong to leave on the table for now.

Whilst the new brand and our website was extremely impactful, building a website with SquareSpace added additional costs in the form of a £204 a year Squarespace subscription and £16 a year for domain registration. Squarespace is a powerful tool but many of the features that would help us in our efforts to move off Meetup such as managing mailing lists and sending mass emails are paywalled. In the long run I’d like us to migrate off Squarespace to avoid trading one bad platform for another.  
We didn’t have as many opportunities to collaborate and for cross promotion with other communities as I would have liked. We started providing a slot in our event for other communities to promote their community announcements but there was virtually zero take up for this after the first time we did this.

## Conclusion

Meetup is still Terrible: expensive, unreliable, and plagued with bad user experience. Still though there was a lot we could do better to make our Meetup a success and avoid terrible events with very low attendance and engagement.  
We haven’t yet been able to execute a full move off of Meetup so it's unclear whether moving off Meetup entirely would have been beneficial \- although the continued growth of our community on the platform would suggest otherwise. Adding Luma as a platform didn’t hurt but did contribute to workload for our organisers with replicated effort for each additional platform. The rebrand drove new engagement although without directly surveying our volunteers or attendees it’s hard to conclusively link the spike in growth with the new brand.

My approach to measuring metrics of success made it hard to decouple the result of each specific action but overall the result has been positive. Rebranding and parallel promotion of events to Luma definitely helped revive our community but did not measurably reduce our reliance on Meetup. Collaboration was great for bringing some new energy into our community but the impact of our collaboration efforts was hard to measure.

Yes, Meetup is terrible, but by doing things differently our community got back to growing and hosting great AI talks for our community.

## Next Steps

I’m working with the awesome team at PyData London in an effort to learn how to coordinate our growing team of volunteers at AI Signals. I've learned a lot from volunteering about building teams around trust with PyData and may write up some of this work in future. 

At Signals we’re figuring out how to make the most of our regained momentum, considering setting up an LLC to allow us to transact, building new partnerships with sponsors, and scaling the number of events we’re able to deliver.

---

If you’re a community organiser I hope this article had some useful insights into our experiences trying to move away from Meetup. I’d love to hear from you about your experiences as an organiser, please join the community over at [notanother.pizza](http://notanother.pizza) and join the conversation.