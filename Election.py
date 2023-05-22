
import string, random, math, pandas as pd

class Election:
    def __init__(self, num_winners=1, ballots_df=None, num_candidates=8, num_observations=10000):
        self.num_winners = num_winners
        self.ballots_df = ballots_df if ballots_df else self.create_submitted_ballots(num_candidates, num_observations)
        self.log(f'{len(self.ballots_df):,} ballots received.')
        self.ballots_df = self.append_columns(self.ballots_df)

        self.cnt_iterations = 0
        self.results = {'Winners':[]}

    def log(self, msg):
        print(f'\n{msg}\n')

    def display_ballots(self):
        return self.ballots_df

    def display_winners(self):
        self.log(f"Winner(s): {', '.join(self.results['Winners'])}")

    def create_submitted_ballots(self, num_candidates, num_observations):
        # Create list of 'Candidate A', 'Candidate B', etc. for num_candidates.
        names = [f'Candidate {x}' for x in string.ascii_uppercase[:num_candidates]]
        names.reverse()
        names.append(None)

        # Create ballots that rank candidates.
        # The rank is produced by randomly pulling candidates from the weighted list.
        # 'None' cannot be a first choice, nor can any choices be made after 'None'.
        ballot_results_raw = []
        for _ in range(num_observations):
            obs = []
            while len(obs) < num_candidates:
                obs_spread = names.copy()
                random.shuffle(obs_spread)
                if len(obs) == 0:
                    next_choice = None
                    while next_choice == None:
                        next_choice = obs_spread.pop()
                elif obs[-1] == None:
                    next_choice = None
                else:
                    unacceptable = True
                    while unacceptable:
                        next_choice = obs_spread.pop()
                        unacceptable = next_choice in obs
                obs.append(next_choice)
            ballot_results_raw.append(obs)

        # Name columns as Choice_1, Choice_2, etc.
        ballot_resutls = pd.DataFrame(data=ballot_results_raw, columns=[f'Choice_{i+1}' for i in range(len(names)-1)])

        # Reset index to start at 1 instead of 0.
        ballot_resutls.index += 1

        # Rename index as 'Ballot_ID'.
        ballot_resutls.index.rename('Ballot_ID', inplace=True)

        return ballot_resutls
        
    def append_columns(self, df, perc_challenged=5):
        # Create 'Is_Challenged' and 'Is_Resolved' columns.
        #   'Is_Resolved' is 'None' if no challenge has been made.
        df['Is_Challenged'], df['Is_Resolved'] = False, None

        # Create challenges for appx. 5% of ballots.
        # All challenged ballots are marked as resolved. These columns
        #   are demonstrative only and don't affect the calculation.
        for _ in range(1,math.ceil(1+len(df)*perc_challenged/100)):
            index = random.randrange(1,len(df))
            df.loc[index,('Is_Challenged','Is_Resolved')] = True, True
        return df

    def analyze_ballots(self):
        df, num_winners = self.ballots_df, self.num_winners

        # Drop columns not relevant to determining the winner(s).
        df = df.drop(columns=[c for c in df.columns if not c.startswith('Choice_')], axis=1)
        while True:
            self.cnt_iterations += 1

            # This is the magic behind SVT/RCV: Non-null values fill
            #   toward the Choice_1 column.
            df = df.bfill(axis=1).dropna(axis=0, how='all')

            # Because values fill toward Choice_1, that is the only
            #   column that ever needs to be tallied.
            vc = df['Choice_1'].value_counts()
            self.results[f'Iteration {self.cnt_iterations}'] = vc

            # This voting system can produce multiple winners. A single
            #   winner must have at least 50% of the votes, two winners 
            #   must each have at least 33.3% of the votes, etc.
            if vc.iloc[0] >= len(df)/(num_winners+1):
                val = vc[vc == vc[0]].index[0]
                self.results['Winners'].append(val)

                # When a winner has emerged (by percentage of total votes),
                #   he or she is dropped from the remaining candidates so that
                #   the candidate's voters' second and third choices, etc. can
                #   continue to apply.
                df.replace(val, None, inplace=True)

                # Once all the winners have emerged, the algorithm ends
                if len(self.results['Winners']) == num_winners:
                    self.results['Winners'].sort()
                    self.log(f'Election analyzed in {self.cnt_iterations} iterations.')
                    return
            
            # If this iteration did not produce a winner, the lowest-ranking
            #   candidate(s) is/are removed . . . and the process repeates.
            else:
                for i in vc[vc == vc.min()].index:
                    df.replace(i, None, inplace=True)

    def display_full_results(self):
        res = list(self.results.items())
        res.reverse()
        res.pop()
        for x in res:
            print(x[0])
            for i in x[1:]:
                for j in range(len(i)):
                    print(f'\t{i.index[j]}\t{i[j]}')