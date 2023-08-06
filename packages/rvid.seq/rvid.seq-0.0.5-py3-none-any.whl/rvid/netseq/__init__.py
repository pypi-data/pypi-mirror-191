"""
RID layer on top of networknumbers


Problem A:  You have multiple processes that all want to use RID:s in the same context
Solution A: Issue RID:s from a socket server instead of in-process
Problem B:  The overhead of send/receive on a socket is high enough to be a problem during bursts
Solution B: Issue RID:s in tranches, to amortize the socket overhead across more RID:s.
Problem C:  If many tranches are requested in short time, some of them will deviate a lot from the
            Unix epoch.
Solution C: Plan ahead during tranche issue, and make interleaved tranches based on the number of
            currently known clients.
Problem D:  You need to know how many clients you have, in order to make tranches
Solution D: Keep a dynamic set of requestors. Assume changes are not too frequent. Throw away all
            prepared tranches whenever a new client shows up and make new ones.

"""
