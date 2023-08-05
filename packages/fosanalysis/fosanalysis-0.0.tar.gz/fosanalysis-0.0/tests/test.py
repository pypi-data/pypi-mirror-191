
import matplotlib.pyplot as plt
import numpy as np
import fosanalysis as fa

fa.tensionstiffening.Fischer(2,3,4, knödel=5)

sd = fa.protocols.ODiSI6100TSVFile("examples/data/demofile.tsv")
x = sd.get_x_values()
y = sd.get_y_table()[1]

masker = fa.preprocessing.masking.GradientChange(threshold=250000, radius=2)
grad = masker.gradient_change(x, y, radius=1)
plt.plot(x, grad)
grad = masker.gradient_change(x, y, radius=2)
plt.plot(x, grad)
plt.show()

clean = masker.run(x, y)
plt.plot(x, masker.SRA_list)
plt.show()
plt.plot(x, y)
plt.plot(x, clean)
plt.show()

print("Done")