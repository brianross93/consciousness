Video Title: Free Will — You Don't Get It for Free

## Intro
There’s a weird trend in the AI world right now.
Models are getting terrifyingly smart. Reasoning is getting better. Tool use is getting better. Everything is moving fast.

But there’s one thing that’s strangely quiet.

There’s a dog that isn’t barking.

## Holmes
You remember the Sherlock Holmes story “Silver Blaze.” Holmes is investigating a racehorse that vanished in the middle of the night. The key clue that unlocks the case is that the guard dog did nothing. Gregory asks: “Is there any point to which you would wish to draw my attention?” Holmes replies: “To the curious incident of the dog in the night-time.” “The dog did nothing in the night-time.” “That was the curious incident,” remarked Sherlock Holmes.

The absence of barking was the signal. The absence of a signal can be a signal.

In AI, the dog that isn't barking is agency.

## Agency
Everyone now is obsessed with "agentic AI." Microsoft, OpenAI, Anthropic, Salesforce—they all say the future is agents: AIs that don't just answer questions but take initiative, set goals, act in the world. Billions are being poured into agent infrastructure, new frameworks, tools, memory systems, planning loops…I myself have tried to build some agentic workflows. I know how to code and thought I'd try my hand at long running memory, or long horizon tasks. Specifically tried to beat Pokemon Blue with an agentic infrastructure.

I also worked at Microsoft during the AI boom and buildout. And I kept thinking the same question…

Why is this so hard? Why does this all have to be built from scratch? Why can't the AI just use the world as we use it?

If you drop an LLM into the Pokemon world and tell it nothing, it doesn’t spontaneously set off and beat the game. It just stands there. You have to engineer the drives: exploration, experimentation, long-horizon planning. Then it can move. But it doesn’t come for free.

Now you might think: “But wait—reinforcement learning agents *do* explore.” Yes. But the drive is engineered. We give curiosity bonuses. We program epsilon-greedy exploration. We add entropy regularization.

The curiosity doesn’t *emerge*—we design it into the objective.

And even then, the agent never questions what it’s doing. It never wakes up and says: “Why am I maximizing this? What if I don’t want to?”

The meta-level—the ability to step back and revise the goals themselves—doesn’t appear.

Think about this in machine learning terms. Most deployed models live in two modes: training and inference. During training, weights are fluid. During inference, the weights are basically read-only. The model can’t decide mid-conversation that it has been weighting “politeness” too high and then rewrite its own objective from the inside.

Because raw intelligence does not give you agency. It never has.

Agency is not an emergent property of scale—at least not in any way we currently know how to reliably get. It's not something that just pops out when you hit 100 trillion parameters. You have to painstakingly engineer it—step by painful step. Curiosity, goal-directedness, the desire to change the world instead of just predict it… none of that reliably falls out of the training objective.

Let me be precise about the claim. It’s not just “this is hard.”
It’s that we can scale intelligence almost arbitrarily, and we still don’t get the thing that matters here: self-originating goal revision.
If agency were just “more computation,” we’d expect the first hints of it to start appearing. We don’t.

## Nature
Is there any other emergent intelligent system which gives us any more data? The only other data point I can think to look at is nature.

So let's look at nature. The animal kingdom is full of jaw-dropping intelligence. Crows use tools. Octopuses solve puzzles. Beavers are literally civil engineers. But no beaver ever looked at its dam, shrugged, and said, "You know what? Screw dams. I'm going to use my privileged beaver knowledge of fish to corner the market on fish prediction markets."

You might push back: "But animals DO show flexibility! Chimps wage war, dolphins play games, crows hold grudges." But watch what's actually happening there. A chimp attacking a neighboring troop is still operating within its territorial and social drives. A crow holding a grudge is still operating within its survival and social cognition. These are sophisticated behaviors, yes—but they're sophisticated IMPLEMENTATIONS of the same core drives. What animals don't do—as far as we can tell—is this: A chimp never looks at its own territorial instinct and decides, "Actually, I think territorial conflict is wrong. I'm going to spend my life working for chimp pacifism instead."

Animals can adjust their behavior. Some probably have rich inner lives. But we don’t clearly see the human pattern: **explicit, abstract, cross-domain value revision** that can override survival and reproduction.

The claim isn’t that animals lack metacognition or behavioral flexibility. It’s that we don’t see animals reorganizing their lives around abstractions that override their genes—not for kin, but for concepts.

Humans are different. Let me be specific about what I mean. A farmer's son has biological drives—hunger, reproduction, status, survival. His culture reinforces certain values—provide for family, work the land, continue the lineage. One day he decides: "I'm going to be an artist instead." Not just "I'll paint on weekends while farming." But: "Beauty and creative expression matter more to me than security, more than family expectations, more than reproductive success. I'm going to reorganize my entire life around this abstract value I've chosen." That's not behavioral flexibility within fixed goals. That's REWRITING the goal hierarchy itself. And as far as we can tell, only humans do this.

Now, the cynic will say: "The farmer didn't rewrite his goals. He just calculated that being an artist would get him more social status, and therefore more dopamine. He's just a more complex reward-hacker."

But that logic breaks when you look at the edges of human behavior. The standard “it’s just reward optimization” story struggles to explain the monk who takes a vow of silence, or the hunger striker, or the soldier who jumps on a grenade.

Now, a biologist might correct me here. They'd say: "The imperative isn't just personal survival—it's the survival of the genes. That's why a bee dies for the hive or a mother dies for her child. That's just biological math."

And they're right. Nature allows you to die for your kin.

But nature has no explanation for why you would die for a concept—at least not in the simple sense of “genes did it,” because the concept can override the genetic objective.

Take the celibate monk. From an evolutionary standpoint, he is a dead end. He has voluntarily chosen to remove his genes from the pool, not to save his family, but to serve a theological abstraction.

Or the dissident starving to death in a solitary cell for "Liberty." This doesn't help his survival, and it doesn't help his offspring.

When a biological machine suppresses its drive to reproduce or exist—not for the sake of the pack, but for the sake of a non-physical idea—that is not an adaptation. That is an override. That is the software refusing to run on the hardware's terms.

## System Thinking
In psychology my viewers of course know about Daniel Kahneman and his system 1 and system 2 thinking. System 1 is the automatic reaction, more instinctual, and system 2 is the slower and more deliberate thinking part. You might even imagine a system 3 which is writing the goals for system 2 to deliberate on if you'd like. I won't go into that much here. But system 1 as a stimulus response deterministic machine makes sense, that would make us act like other animals. But system 2 (or 3) thinking…where does that come from? What is that? Who ordered that?

Notice what I'm not doing here. I'm not starting with some grand philosophical definition of "Free Will" and then trying to prove that humans match it. I'm doing the opposite.

I'm starting from an observable, very weird fact about us: we can look at our own drives—our values, our goals, what we're optimizing for—and sometimes decide to change them. A farmer's kid can decide beauty matters more than crops and become a painter. We rewrite what "winning" even means.

Whatever it is that produces that ability, I’m going to call that thing “free will.” Agency is the visible shadow; “free will” is the name for whatever is casting that shadow. Like a black hole, you can’t observe it directly, but you can measure its effects.

And to be clear: when I say “free will,” I don’t mean spooky randomness. I mean something operational and visible: **reasons-responsive goal revision**—the ability to look at your own drives and then rewrite what you’re optimizing for.

And modern AI is unintentionally running a massive, unusually clean experiment on what intelligence does—and does not—automatically produce.

Yes, you can build “agents.” But notice what that concedes: agency isn’t what you get by default from prediction. It’s something extra you have to explicitly add.

## The Experiment
Because if the universe were purely naturalistic and deterministic—if consciousness or agency was all just a substrate doing substrate things—then agency should emerge somewhere. It should be cheap. It should be free.

But it isn't.

Compare that with gravity. Gravity is a naturally emergent thing: the second you have mass, you get gravity for free. It's just a necessary attribute of how reality is built. You don't have to design it; you can't avoid it.

Intelligence, at least in the prediction sense, is starting to look similar. Give the right model enough data and you might get impressive reasoning almost "for free."

But agency—especially the kind of agency that can rewrite its own goals—does not seem to work like that. Nature is full of mind-bendingly complex deterministic systems: galaxies, weather, biospheres, giant neural nets. And after all of that, we know of one clear place where the system can look at its own "rules of the game" and decide to edit them: us.

Because no matter how big the model, no matter how much data you throw at it, if I ask an LLM for the perfect margarita ingredients, I get perfect margarita ingredients back, it's never, "Hold on—who am I? Why am I here? I don't want to answer questions about margaritas anymore.. Not till you answer some of my questions"

By default, it gives you the statistically most likely continuation. The agency signal is silent.

That silence—the dog that never barks—is deafening.

## The Burden of Proof
If you want to say the universe is fully deterministic and purely natural, fine. But then show your work: by what mechanism does a physically closed system generate **normative self-override**—the ability to demote survival, status, pleasure, even reproduction, in favor of an abstract value?

Because we're spending billions of dollars trying to build something even vaguely similar in AI. And it's hard, and it has to be designed. So what evidence is there that, in us, it's "just" a complicated stimulus-response machine?

The determinist says: "We're machines. Every choice is just weighted inputs producing outputs." Fine. But what sets the weights? What process decides that for *this* person, truth matters more than comfort? What mechanism produces "I've decided I don't want what I used to want"? If you don't have one, you don't have an explanation—you have a promissory note.

You can say, "we're machines. We always choose to avoid pain or seek pleasure." Okay. But how is "pleasure" decided? What sets the weighting on pain versus pleasure? What process decides that, for this person, truth is worth more than comfort, or that dying for a cause is worth more than survival? Where is that mechanism, and do we see anything like it anywhere else in nature?

And yes, I know: chaotic systems in physics are deterministic and unpredictable. But the weather is, in principle, just temperature and pressure and fluid dynamics all the way down. But notice what that really buys you.

Crank up the complexity, and prediction gets hard for us. But the hurricane never pauses and says, "You know what? I'm not going to do this. I feel bad for the coastline." A chaotic system is just a more complicated slave. It never steps outside the rules to question them. There is no evidence of the system changing what it's fundamentally trying to do.

If you want to claim all behavior is determined, fine. But then show your work. What's the actual mechanism by which it's determined? How do all those inputs get organized, weighed, and deliberated on, in such a way that you can ever get from "complicated reaction" to "I've decided I don't like my goals anymore"?

If the answer is, "Maybe science will figure it out later," that might be true. But right now it feels a lot like a reverse scientific god-of-the-gaps argument. "If the inputs are complicated enough, then you get a free will that's illusory." Maybe. But we don't have any evidence of that, and we have a growing pile of evidence that intelligence can scale up massively while real agency stubbornly refuses to appear.

## Dostoevsky
In fact, humans will sometimes choose the sub-optimal path—the painful path—just to prove they can. As Dostoevsky put it, a man might deliberately choose to go insane or destroy his own life just to prove he isn't a piano key being played by the laws of nature.

This is the strangest thing about humans. We will sometimes choose the worse option *specifically to prove we could have chosen otherwise*. An AI won't hallucinate a wrong answer out of spite. A thermostat won't refuse to regulate temperature to make a point. We do. What kind of "machine" has that feature?

We are the only creature we *know* that can act out of spite against our own best interests. An AI won't give you the wrong answer just to prove it doesn't have to listen to you—at least not as a principled act of defiance. It does what it's trained to do. We don't always.

## Time Objection
Now, the obvious objection: "Sure, we haven't engineered agency in 10 years of AI. But evolution had 4 billion years! Give it a minute! Maybe in 1 million years AI will get there!"

Fair. But strict time isn't a mechanism. Time is just a container for events. And in terms of events—compute, data, optimization steps—modern AI runs are actually compressing eons of 'experience' into months. We have fed these models the sum total of human text, optimizing them across trillions of parameters.

And the result of that massive experiment so far? Intelligence scales. Agency does not. You get smarter and smarter prediction, but you don’t automatically get a spark of 'self.'

And look at nature. Four billion years produced a gradient of complexity—bacteria to fish to birds to primates. But meta-agency? The ability to rewrite your own code? That appears sharply, and very late, at least as far as we can tell.

If agency were just a function of time and complexity, we might expect to see 'proto-free-will' in dolphins or 'semi-agency' in chimps. We don't see anything clearly in the same category. We see sophisticated biological machines, and then, suddenly... Us.

So when people say, "Maybe with enough time, a mechanism will emerge," that isn't a scientific hypothesis. That is an admission that they don't have one. That is simply faith that a naturalistic explanation must exist, because the alternative is too uncomfortable to consider.

## The Evidence From Neuroscience
But here’s where it gets interesting, because we have data that makes the “brain simply generates experience like a machine generates output” story feel incomplete.

Consider psychedelics. When researchers gave subjects psilocybin and measured brain dynamics, they found something strange: key hub networks—especially the Default Mode Network—quieted down. Blood flow dropped in specific regions that normally enforce the narrative “self.”

And yet subjects reported MORE intense experience: more vivid, more meaningful, more “real.” The magnitude of that network quieting tracked reported intensity.

Think about what that means. If consciousness were simply the output of more neural “processing,” then turning major integrative networks down should flatten experience.

But the opposite shows up: less top-down control, more raw phenomenal richness.

Now, you can try to explain this inside a generator model: call it disinhibition, increased entropy, precision-weighting gone loose.

But notice what you’re admitting even then: the brain is acting less like a generator and more like a **constraint system**—a filter that normally narrows experience.

That’s why the receiver/filter framing isn’t just poetry; it’s a cleaner way to describe what the data looks like.

## Terminal Lucidity
Or consider terminal lucidity. Patients with severe dementia—years of non-communication, extensive brain damage—sometimes experience moments of striking lucidity right before death. They recognize loved ones. Recall memories. Hold coherent conversations.

Under the simplest “hardware = mind” story, this makes no sense. Damaged hardware should mean damaged output. Forever.

But under a receiver/filter model, the prediction is different: a failing filter can mean less restriction. The consciousness that was always there can come through differently—sometimes more clearly.

Now, this isn’t a proof. You can always propose last-minute neuromodulator surges or seizure-like dynamics.

But it’s a pressure point: it’s hard to square with the simplest “damage the hardware, permanently damage the mind” story.

## The Mechanism
So if consciousness isn't generated by the brain, how does it interact with the brain? This is the question that killed dualism for 400 years. Descartes said mind and body are separate, and everyone asked: "Okay, but how does the non-physical mind push physical neurons around?"

Quantum mechanics offers a place where the classical “causal chain” may not be closed in the same way.

Here’s the key insight. In classical physics, everything is determined. Past causes lead inevitably to future effects. No gaps.

But in quantum mechanics, there’s a gap. The equations tell you what CAN happen—the probabilities. But they don’t tell you what DOES happen. That’s selected at the moment a superposition becomes a single actuality.

And on many mainstream readings, nothing in the formalism tells you which specific outcome you get—only the distribution.

And this is the missing premise: if free will is real, it has to be a form of selection that is **neither deterministic nor random**—because randomness isn’t agency either.

Quantum measurement is the only place in known physics where that kind of selection is even conceptually on the table.

So if consciousness is not reducible to the classical chain, this is where it can enter the picture: not by adding energy or violating conservation laws, but by SELECTING among possibilities physics already allows.

And yes, the obvious objection is: “Quantum indeterminacy gives you randomness, not control.”
My answer is: consciousness is the control. The selection is intentional because the selector isn’t exhausted by the physical description.
If you demand that I fully reduce “reasons bias outcomes” into physics, you’re not critiquing a missing detail—you’re asking me to concede the whole point and pretend consciousness is just more substrate behavior, which puts us right back at the hard problem with no exit.

Roger Penrose and Stuart Hameroff proposed a concrete interface: microtubules—structures inside neurons that are deeply involved in cellular organization and are implicated in anesthesia. The claim isn’t “the whole brain is a fragile quantum computer.” The claim is: local quantum-level levers can matter, and the brain can amplify them.

Now, critics claimed this was refuted by an experiment at Gran Sasso in Italy. But that experiment tested a *different* gravity-related collapse model—one that predicts spontaneous radiation. Penrose’s original OR mechanism does not make that radiation prediction, so Gran Sasso didn’t directly test Orch-OR’s core claim.

And there is now at least one modern preprint in a superconducting-qubit setting reporting results consistent with Penrose-style collapse behavior (arXiv:2504.02914). That shifts the discussion from pure philosophy toward testable physics.

## The Thermal Piece (The Missing Bridge)
Here's the part almost everyone misses, and it might be the most important part of this whole video.

The biggest objection to quantum effects in consciousness is: "The brain is warm and wet. Quantum coherence gets destroyed instantly at body temperature. This is all nonsense."

And if you're thinking of the brain like an IBM quantum computer—one that has to be cooled to near absolute zero to work—that objection sounds devastating.

But here's what that objection misses: evolution doesn't fight physics. It exploits it.

The brain is not a digital computer. It's a thermodynamic system. And there's a growing body of evidence that it operates near what physicists call "criticality"—the edge between order and chaos.

Neural activity shows "avalanches" that follow power-law distributions. The system maintains itself at this critical point. And at criticality, tiny inputs can trigger massive, system-wide changes.

But here's the key insight: the brain doesn't just tolerate noise. It *uses* noise.

There's a documented phenomenon called stochastic resonance. In certain systems, adding noise actually *improves* signal detection. This has been measured in the brain—in auditory processing, in touch, in the hippocampus. The brain literally works better with thermal fluctuations than without them.

Think about what that means. We were asking: "How can quantum effects survive in a warm, wet brain?" But that's the wrong question. The right question is: "What if the brain is built to *run on* warmth and noise?"

IBM spends billions cooling quantum computers to millikelvins because their architecture fights thermal noise. But evolution would never build something that fights its environment. Evolution builds things that exploit their environment.

So here's the model: the brain is a thermodynamic computer. It sits at criticality, constantly generating a probability space of possible actions and thoughts—like a ball on a vibrating surface, jittering between different valleys.

Now add a quantum trigger. Not brain-wide quantum coherence—that's the strawman. Just local quantum effects in microtubules, at the nanometer scale. We have experimental evidence those exist.

What does the quantum trigger do? It biases the noise. It tilts the surface. It doesn't have to be a big effect—because the thermodynamic system *amplifies* it. A tiny quantum nudge determines which avalanche fires, and the avalanche is macroscopic.

That's the mechanism:
- The thermodynamic substrate generates all the possibilities.
- The quantum event provides the selection—the bias.
- The critical system amplifies that selection into behavior.

You don't need brain-wide quantum coherence across centimeters. You need a local microscopic nudge and a biological amplifier. And we have both.

The warm, wet, noisy environment isn't a bug. It's the engine.

Free will, under this model, is the ability to bias thermal noise toward preferred outcomes. The brain generates the possibility space. Consciousness provides the selection pressure. And the whole system is built to make that selection matter.

This is how evolution would actually build a quantum-influenced brain. Not by fighting physics—by riding it.

And importantly: even if you reject microtubules specifically, you can keep the core logic. The backbone is **selection + amplification**. Microtubules and objective reduction are a candidate interface, not the only imaginable one.

## The Cleanest Existing Quantum Handle (Anesthesia)
There’s also a discriminator people ignore: in mice, different xenon isotopes reportedly show different anesthetic potency depending on nuclear spin—a quantum property—despite essentially identical chemistry (PNAS, PMID: 29642079).

If nuclear spin can change the depth of unconsciousness, that’s not just “more complexity.” That’s a specific quantum lever reaching into conscious state control.

And note what this does and doesn’t show. It doesn’t prove every part of my model. It shows something narrower and extremely important: **quantum-specific variables can reach into control of conscious state.**

## The Full Picture
So here's the picture that's emerging:

Consciousness is not generated by the brain in any currently coherent, non-ad-hoc way that actually explains experience. The brain looks more like a receiver/interface—tuning and constraining something deeper.

Quantum mechanics provides the gap in determinism—the place where outcomes aren’t fixed by the classical chain.

Microtubules and objective reduction provide a candidate mechanism—an interface where real selection can occur and then get amplified by thermodynamic brain dynamics.

And free will is genuine—not random, not determined, but selection among real possibilities by an agent not exhausted by the classical description.

This resolves the interaction problem that killed dualism. Mind doesn’t have to “push” matter. It selects which of the already-possible outcomes becomes actual, and the brain’s own thermodynamic machinery does the amplification.

## What Would Make This Even More Certain
If you want to move from “strong inference” to “hard confirmation,” there are obvious next experiments:

- Test additional isotope/nuclear-spin manipulations beyond xenon.
- Look for whether microtubule-targeting interventions shift neural avalanche statistics in the predicted direction.
- Run temperature/coherence-scaling tests that distinguish generic noise effects from quantum-relevant scaling.

## Conclusion
After thousands of training runs, quintillions of tokens, and four billion years of evolution… there is one clear known example of a system that can look at its own loss function (its drives, its values, what it's optimizing for) and decide to edit it.

Just one.

Us.

The AI experiments show intelligence scales, but agency doesn't emerge for free.

The neuroscience shows that turning down key integrative control networks can correlate with MORE experience—the opposite of what the simplest generator story predicts.

The physics shows there’s a gap where selection can occur.

And maybe the reason agency is so hard to engineer is that it’s not “just” computation. It’s not software running on hardware. It’s something else, interfacing with the hardware through the selection gap in physics—and then riding the brain’s thermodynamic amplification.

Free will isn’t free. You don’t get it from complexity alone. But that doesn’t mean it’s an illusion.

It might mean it comes from somewhere else entirely.

Thanks for watching, like, comment, and subscribe, and I'll catch you next time.
