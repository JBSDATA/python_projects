''' how does your spend compare to this guideline?

- Giving ( 10% )
- Saving ( 10% )
- Food ( 10-15% )
- Utilities ( 5-15% )
- Housing ( 25% )
- Transportation ( 10% )
- Health ( 5-10% )
- Insurance ( 10-25% )
- Recreation ( 5-10% )
- Personal Spending ( 5-10% )
- Misc ( 5-10% )

 '''

import numpy as np

# total pay
gross_pay = 5490.19

#### Taxes
OASDI = 308.14
medicare = 72.07
state_tax = 515.21
fed_tax = 242.75

total_tax = np.sum([OASDI, medicare, state_tax, fed_tax])

post_tax_total = gross_pay - total_tax

##### Insurance

# plan with what we currently have elected. Anything less will be great ( no longer paying family plan, just Sophia )
dental_ins = 60.35
medical_ins = 437.41
vision_ins = 23.32
total_ins = np.sum([dental_ins, medical_ins, vision_ins])
current_ins_perc = total_ins/post_tax_total
sophia_ins = total_ins * (1/3)
.15*post_tax_total
current_ins_perc

############################ SAVING -> Aim for 20% right now

#### 401k
roth = 274.51
roth/post_tax_total

#### Capital Group - Sophia's College Fund
college_fund = 300
college_fund/post_tax_total

#### Personal Savings
personal_savings = 300
college_fund/post_tax_total


total_savings = np.sum([roth, college_fund, personal_savings])
total_savings / post_tax_total

post_tax_total - total_savings


################################ Rent  / housing / utilities
max_rent = post_tax_total*.20
utilities = .10 * post_tax_total
rent_and_utilities = np.sum([max_rent, utilities])

post_tax_total - total_savings - rent_and_utilities


############## child support
max_child_support = 1100
sophia_fund_and_ins = sophia_ins + college_fund
addtl_monthly_child_support =  max_child_support - sophia_fund_and_ins


'''  After Insurance, Saving, Rent/Utilities, and child support....

We have the following amount left for:
- Food
- Transportation ( car needs repair, gas and depreciation )
- Health
- Recreation

'''

food_transportation_recreation_amt = post_tax_total - total_ins - total_savings - rent_and_utilities - addtl_monthly_child_support

food = 400
car = 250 # gas and whatever is left over should go towards depreciation
recreation = 300

food_transportation_recreation_amt - np.sum([food, car, recreation])


''' if anything, you will have more than the remaining amount above. Why?
#### 1. Child support will not be $1,100 maybe a couple hundred less
#### 2. Insurance will be several hundred less once Karishma finds her own insurance

As your career grows, you can put more into the savings account for Sophia as well as for yourself and into investing.

'''




################### Depreciation
