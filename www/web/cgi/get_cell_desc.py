#!/bin/bash
"source" "/home/wdeng3/scARE/bin/activate"
"python" "$0" "$@"
##############################
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-04-14 14:57:27
 # @modify date 2023-04-14 14:57:27
 # @desc [description]
#############################
import cgitb
import pandas as pd
import cgi
import json
# import MySQLdb
cgitb.enable()
print( 'Content_Type:text/json; charset=utf-8\r\n\n')


form = cgi.FieldStorage()
cell=form['Cell'].value


## TODO : add the cell type information
des='Introduction of cell'
if cell=='Ex' or cell=='In':
    des='''
<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output">
<style data-mw-deduplicate="TemplateStyles:r1066479718">.mw-parser-output .infobox-subbox{padding:0;border:none;margin:-3px;width:auto;min-width:100%;font-size:100%;clear:none;float:none;background-color:transparent}.mw-parser-output 
    .infobox-3cols-child{margin:auto}.mw-parser-output .infobox .navbar{font-size:100%}body.skin-minerva .mw-parser-output .infobox-header,body.skin-minerva .mw-parser-output .infobox-subheader,body.skin-minerva .mw-parser-output 
    .infobox-above,body.skin-minerva .mw-parser-output .infobox-title,body.skin-minerva .mw-parser-output .infobox-image,body.skin-minerva .mw-parser-output .infobox-full-data,body.skin-minerva .mw-parser-output .infobox-below{text-align:center}</style>
<p>Within a <a href="https://en.wikipedia.org/wiki/Nervous_system" title="Nervous system">nervous system</a>, a <b>neuron</b>, <b>neurone</b>, or <b>nerve cell</b> is an <a href="https://en.wikipedia.org/wiki/Membrane_potential#Cell_excitability" title="Membrane potential">electrically excitable</a> <a href="https://en.wikipedia.org/wiki/Cell_(biology)"
     title="Cell (biology)">cell</a> that fires electric signals called <a href="https://en.wikipedia.org/wiki/Action_potentials" class="mw-redirect" title="Action potentials">action potentials</a>. Neurons communicate with other cells via <a href="https://en.wikipedia.org/wiki/Synapse" 
     title="Synapse">synapses</a> - specialized connections that commonly use minute amounts of chemical <a href="https://en.wikipedia.org/wiki/Neurotransmitter" title="Neurotransmitter">neurotransmitters</a> to pass the electric signal from the presynaptic neuron to the target cell through the synaptic gap. 
     The neuron is the main component of <a href="https://en.wikipedia.org/wiki/Nervous_tissue" title="Nervous tissue">nervous tissue</a> in all <a href="https://en.wikipedia.org/wiki/Animalia" class="mw-redirect" title="Animalia">animals</a> except <a href="https://en.wikipedia.org/wiki/Sponge" title="Sponge">sponges</a> and <a href="https://en.wikipedia.org/wiki/Placozoa" 
     title="Placozoa">placozoa</a>. Non-animals like <a href="https://en.wikipedia.org/wiki/Plant" title="Plant">plants</a> and <a href="https://en.wikipedia.org/wiki/Fungi" class="mw-redirect" title="Fungi">fungi</a> do not have nerve cells.
</p><p>Neurons are typically classified into three types based on their function. <a href="https://en.wikipedia.org/wiki/Sensory_neuron" title="Sensory neuron">Sensory neurons</a> respond to <a href="https://en.wikipedia.org/wiki/Stimulus_(physiology)" title="Stimulus (physiology)">stimuli</a> such as touch, sound, or 
light that affect the cells of the <a href="https://en.wikipedia.org/wiki/Sense" title="Sense">sensory organs</a>, and they send signals to the spinal cord or brain. <a href="https://en.wikipedia.org/wiki/Motor_neuron" title="Motor neuron">Motor neurons</a> receive signals from the brain and spinal cord to control everything 
from <a href="https://en.wikipedia.org/wiki/Muscle_contraction" title="Muscle contraction">muscle contractions</a> to <a href="https://en.wikipedia.org/wiki/Gland" title="Gland">glandular output</a>. <a href="https://en.wikipedia.org/wiki/Interneuron" title="Interneuron">Interneurons</a> connect neurons to other neurons within the same region of the 
brain or spinal cord. When multiple neurons are functionally connected together, they form what is called a <a href="https://en.wikipedia.org/wiki/Neural_circuit" title="Neural circuit">neural circuit</a>.
</p><p>A typical neuron consists of a cell body (<a href="https://en.wikipedia.org/wiki/Soma_(biology)" title="Soma (biology)">soma</a>), <a href="https://en.wikipedia.org/wiki/Dendrite" title="Dendrite">dendrites</a>, and a single <a href="https://en.wikipedia.org/wiki/Axon" title="Axon">axon</a>. The soma is a compact structure, and the axon and 
dendrites are filaments extruding from the soma. Dendrites typically branch profusely and extend a few hundred micrometers from the soma. The axon leaves the soma at a swelling called the <a href="https://en.wikipedia.org/wiki/Axon_hillock" title="Axon hillock">axon hillock</a> and travels for as far as 
1 meter in humans or more in other species. It branches but usually maintains a constant diameter. At the farthest tip of the axon's branches are <a href="https://en.wikipedia.org/wiki/Axon_terminals" class="mw-redirect" title="Axon terminals">axon terminals</a>, where the neuron can transmit a signal 
across the <a href="https://en.wikipedia.org/wiki/Synapse" title="Synapse">synapse</a> to another cell. Neurons may lack dendrites or have no axon. The term <a href="https://en.wikipedia.org/wiki/Neurite" title="Neurite">neurite</a> is used to describe either a dendrite or an axon, particularly when the cell is 
<a href="https://en.wikipedia.org/wiki/Cellular_differentiation" title="Cellular differentiation">undifferentiated</a>.
</p><p>Most neurons receive signals via the dendrites and soma and send out signals down the axon. At the majority of synapses, signals cross from the axon of one neuron to a dendrite of another. However, synapses can connect an axon to another axon or a dendrite to another dendrite.
</p><p>The signaling process is partly electrical and partly chemical. Neurons are electrically excitable, due to maintenance of <a href="https://en.wikipedia.org/wiki/Voltage" title="Voltage">voltage</a> gradients across their <a href="https://en.wikipedia.org/wiki/Cell_membrane" title="Cell membrane">membranes</a>. If the voltage
 changes by a large enough amount over a short interval, the neuron generates an <a href="https://en.wikipedia.org/wiki/All-or-none_law" title="All-or-none law">all-or-nothing</a> <a href="https://en.wikipedia.org/wiki/Electrochemical" class="mw-redirect" title="Electrochemical">electrochemical</a> pulse called an 
 <a href="https://en.wikipedia.org/wiki/Action_potential" title="Action potential">action potential</a>. This potential travels rapidly along the axon and activates synaptic connections as it reaches them. Synaptic signals may be <a href="https://en.wikipedia.org/wiki/Excitatory_postsynaptic_potential" 
 title="Excitatory postsynaptic potential">excitatory</a> or <a href="https://en.wikipedia.org/wiki/Inhibitory_postsynaptic_potential" title="Inhibitory postsynaptic potential">inhibitory</a>, increasing or reducing the net voltage that reaches the soma.
</p><p>In most cases, neurons are generated by <a href="https://en.wikipedia.org/wiki/Neural_stem_cell" title="Neural stem cell">neural stem cells</a> during brain development and childhood. <a href="https://en.wikipedia.org/wiki/Neurogenesis" title="Neurogenesis">Neurogenesis</a> largely ceases during 
adulthood in most areas of the brain.
</p>
</div>
</div>
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Neuron">"Neuron"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
if cell=='Mic':
    des='''
    <p><b>Microglia</b> are a type of <a href="https://en.wikipedia.org/wiki/Neuroglia" class="mw-redirect" title="Neuroglia">neuroglia</a> (glial cell) located throughout the <a href="https://en.wikipedia.org/wiki/Brain" title="Brain">brain</a> and <a href="https://en.wikipedia.org/wiki/Spinal_cord" title="Spinal cord">spinal cord</a>.
     Microglia account for about 10-15% of cells found within the brain. As the resident <a href="https://en.wikipedia.org/wiki/Macrophage" 
    title="Macrophage">macrophage</a> cells, they act as the first and main form of active immune defense in the <a href="https://en.wikipedia.org/wiki/Central_nervous_system" title="Central nervous system">central nervous system</a> (CNS).
    Microglia (and other neuroglia including <a href="https://en.wikipedia.org/wiki/Astrocytes" class="mw-redirect" title="Astrocytes">astrocytes</a>) are distributed in large non-overlapping regions throughout the CNS.
     Microglia are key cells in overall brain maintenance-they 
    are constantly scavenging the CNS for <a href="https://en.wikipedia.org/wiki/Senile_plaques" class="mw-redirect" title="Senile plaques">plaques</a>, damaged or unnecessary <a href="https://en.wikipedia.org/wiki/Neurons" class="mw-redirect" title="Neurons">neurons</a> and <a href="https://en.wikipedia.org/wiki/Synapse" title="Synapse">synapses</a>, 
    and infectious agents. Since these processes must be efficient to prevent potentially fatal damage, microglia are extremely sensitive to even small pathological 
    changes in the CNS. This sensitivity is achieved in part by the presence of unique <a href="https://en.wikipedia.org/wiki/Potassium_channels" class="mw-redirect" title="Potassium
     channels">potassium channels</a> that respond to even small changes in <a href="https://en.wikipedia.org/wiki/Extracellular" class="mw-redirect" title="Extracellular">extracellular</a> potassium.
     Recent evidence shows that microglia are also key players in the sustainment of normal brain functions under healthy conditions.Microglia also constantly monitor neuronal functions through direct 
     somatic contacts and exert neuroprotective effects when needed.
</p>
<p>The brain and spinal cord, which make up the CNS, are not usually accessed directly by pathogenic factors in the body's circulation due to a series of <a href="https://en.wikipedia.org/wiki/Endothelial_cells" class="mw-redirect" title="Endothelial cells">endothelial cells</a> known as the 
<a href="https://en.wikipedia.org/wiki/Blood%E2%80%93brain_barrier" title="Blood-brain barrier">blood-brain barrier</a>, or BBB. The BBB prevents most infections from reaching the vulnerable nervous tissue. In the case where infectious agents are directly introduced to the brain or cross the 
blood-brain barrier, microglial cells must react quickly to decrease <a href="https://en.wikipedia.org/wiki/Inflammation" title="Inflammation">inflammation</a> and destroy the infectious agents before they damage the sensitive neural tissue. Due to the lack of <a href="https://en.wikipedia.org/wiki/Antibodies" 
class="mw-redirect" title="Antibodies">antibodies</a> from the rest of the body (few antibodies are small enough to cross the blood-brain barrier), microglia must be able to recognize foreign bodies, swallow them, and act as <a href="https://en.wikipedia.org/wiki/Antigen-presenting_cell" 
title="Antigen-presenting cell">antigen-presenting cells</a> activating <a href="https://en.wikipedia.org/wiki/T-cells" class="mw-redirect" title="T-cells">T-cells</a>.
</p>
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Microglia">"Microglia"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
elif cell=='Ast':
    des='''
<p><b>Astrocytes</b> 
, also known collectively as <b>astroglia</b>, are characteristic star-shaped <a href="https://en.wikipedia.org/wiki/Glial_cells" class="mw-redirect" title="Glial cells">glial cells</a> in the <a href="https://en.wikipedia.org/wiki/Brain" title="Brain">brain</a> and <a href="https://en.wikipedia.org/wiki/Spinal_cord" title="Spinal cord">spinal cord</a>. 
They perform many functions, including biochemical control of <a href="https://en.wikipedia.org/wiki/Endothelial_cell" class="mw-redirect" title="Endothelial cell">endothelial cells</a> that form the <a href="https://en.wikipedia.org/wiki/Blood%E2%80%93brain_barrier" title="Blood-brain barrier">blood-brain barrier</a>,
provision of nutrients to the nervous tissue, maintenance of extracellular ion balance, regulation of cerebral 
blood flow, and a role in the repair and <a href="https://en.wikipedia.org/wiki/Glial_scar" title="Glial scar">scarring</a> process of the brain and spinal cord following infection and traumatic injuries.
The proportion of astrocytes in the brain is not well defined; depending on the counting technique used, studies have found that the astrocyte proportion varies by region and ranges from 20% to around 40% of all glia. Another study reports that astrocytes are the most numerous cell type in the brain.Astrocytes are the major source of cholesterol
in the central nervous system. Apolipoprotein E transports cholesterol from astrocytes to neurons and other glial cells, regulating cell signaling in the brain.
Astrocytes in humans are more than twenty times larger than in rodent brains, and make contact with more than ten times the number of synapses.
</p>
<p>Research since the mid-1990s has shown that astrocytes propagate intercellular <a href="https://en.wikipedia.org/wiki/Calcium" title="Calcium">Ca<sup>2+</sup></a> waves over long distances in response to stimulation, and, similar to neurons, release transmitters 
(called <a href="https://en.wikipedia.org/wiki/Gliotransmitter" title="Gliotransmitter">gliotransmitters</a>) in a Ca<sup>2+</sup>-dependent manner.Data suggest that astrocytes also signal to neurons through Ca
<sup>2+</sup>-dependent release of <a href="https://en.wikipedia.org/wiki/Glutamate" class="mw-redirect" title="Glutamate">glutamate</a>. Such discoveries have made astrocytes 
an important area of research within the field of <a href="https://en.wikipedia.org/wiki/Neuroscience" title="Neuroscience">neuroscience</a>.
</p>
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Astrocyte">"Astrocyte"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
elif cell=='Oli':
    des='''
    <p><b>Oligodendrocytes</b>, are a type of <a href="https://en.wikipedia.org/wiki/Neuroglia" class="mw-redirect" title="Neuroglia">neuroglia</a> whose main functions are to provide support and insulation to 
    <a href="https://en.wikipedia.org/wiki/Axon" title="Axon">axons</a> in the <a href="https://en.wikipedia.org/wiki/Central_nervous_system" title="Central nervous system">central nervous system</a> of <a href="https://en.wikipedia.org/wiki/Jawed_vertebrates" class="mw-redirect" title="Jawed vertebrates">jawed vertebrates</a>, 
    equivalent to the function performed by <a href="https://en.wikipedia.org/wiki/Schwann_cell" title="Schwann cell">Schwann cells</a> in the <a href="https://en.wikipedia.org/wiki/Peripheral_nervous_system" title="Peripheral nervous system">peripheral nervous system</a>. 
    Oligodendrocytes do this by creating the <a href="https://en.wikipedia.org/wiki/Myelin_sheath" class="mw-redirect" title="Myelin sheath">myelin sheath</a>.
 A single oligodendrocyte can extend its processes to 50 axons,
 wrapping approximately 1&nbsp;um of myelin sheath around each axon; Schwann cells, on the other hand, can wrap around only one axon. Each oligodendrocyte forms one segment of myelin for several adjacent axons.
</p>
<p>Oligodendrocytes are found only in the central nervous system, which comprises the <a href="https://en.wikipedia.org/wiki/Brain" title="Brain">brain</a> 
and <a href="https://en.wikipedia.org/wiki/Spinal_cord" title="Spinal cord">spinal cord</a>.  
These cells were originally thought to have been produced in the <a href="https://en.wikipedia.org/wiki/Neural_tube" title="Neural tube">ventral neural tube</a>; 
however, research now shows oligodendrocytes originate from the <a href="https://en.wikipedia.org/wiki/Ventricular_zone" title="Ventricular zone">
ventral ventricular zone</a> of the embryonic spinal cord and possibly have some concentrations in the forebrain. They are the last cell type to be generated in the 
<a href="https://en.wikipedia.org/wiki/Central_nervous_system" title="Central nervous system">central nervous system</a> (CNS).
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Oligodendrocyte">"Oligodendrocyte"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
elif cell=='OPC':
    des='''<p><b>Oligodendrocyte progenitor cells</b> (<b>OPCs</b>), also known as <b>oligodendrocyte precursor cells</b>, <b>NG2-glia</b>, <b>O2A cells</b>, or <b>polydendrocytes</b>, are a subtype of <a href="https://en.wikipedia.org/wiki/Neuroglia" class="mw-redirect" title="Neuroglia">glia</a> 
    in the <a href="https://en.wikipedia.org/wiki/Central_nervous_system" title="Central nervous system">central nervous system</a> named for their essential role as <a href="https://en.wikipedia.org/wiki/Precursor_cell" title="Precursor cell">precursors</a> to <a href="https://en.wikipedia.org/wiki/Oligodendrocytes" class="mw-redirect"
     title="Oligodendrocytes">oligodendrocytes</a>.They are typically identified by co-expression of <a href="https://en.wikipedia.org/wiki/PDGFRA" title="PDGFRA">PDGFRA</a> and 
     <a href="https://en.wikipedia.org/wiki/NG2_proteoglycan" title="NG2 proteoglycan">NG2</a>.
</p>
<p>OPCs play a critical role in developmental and adult <a href="https://en.wikipedia.org/wiki/Myelinogenesis" title="Myelinogenesis">myelinogenesis</a> by giving rise to oligodendrocytes, which then ensheath <a href="https://en.wikipedia.org/wiki/Axon" title="Axon">axons</a> and provide electrical 
insulation in the form of a <a href="https://en.wikipedia.org/wiki/Myelin" title="Myelin">myelin</a> sheath, enabling faster <a href="https://en.wikipedia.org/wiki/Action_potential" title="Action potential">action potential</a> propagation and high fidelity transmission without a need for an increase in 
axonal diameter.The loss or lack of OPCs, and consequent lack of differentiated oligodendrocytes, is associated with a loss of myelination and subsequent 
impairment of neurological functions. In addition, OPCs express receptors for various <a href="https://en.wikipedia.org/wiki/Neurotransmitters" class="mw-redirect" 
title="Neurotransmitters">neurotransmitters</a> and undergo membrane <a href="https://en.wikipedia.org/wiki/Depolarization" title="Depolarization">depolarization</a> when they receive synaptic inputs from neurons.
</p>
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Oligodendrocyte_progenitor_cell">"Oligodendrocyte progenitor cell"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative
 Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
elif cell=='End':
    des='''<p>The <b>endothelium</b> is a single layer of <a href="https://en.wikipedia.org/wiki/Squamous_epithelial_cell" class="mw-redirect" title="Squamous epithelial cell">squamous</a> <b>endothelial cells</b> that line the interior surface of <a href="https://en.wikipedia.org/wiki/Blood_vessel" 
    title="Blood vessel">blood vessels</a> and <a href="https://en.wikipedia.org/wiki/Lymphatic_vessel" title="Lymphatic vessel">lymphatic vessels</a>. The endothelium forms an
     interface between circulating <a href="https://en.wikipedia.org/wiki/Blood" title="Blood">blood</a> or <a href="https://en.wikipedia.org/wiki/Lymph" title="Lymph">lymph</a> in the <a href="https://en.wikipedia.org/wiki/Lumen_(anatomy)" title="Lumen (anatomy)">lumen</a> and the rest of the vessel wall. Endothelial cells 
     form the barrier between vessels and tissue and control the flow of substances and fluid into and out of a tissue.
</p><p>Endothelial cells in direct contact with blood are called vascular endothelial cells whereas those in direct contact with <a href="https://en.wikipedia.org/wiki/Lymph" title="Lymph">lymph</a> are known as lymphatic endothelial cells. Vascular endothelial cells line the 
entire <a href="https://en.wikipedia.org/wiki/Circulatory_system" title="Circulatory system">circulatory system</a>, from the <a href="https://en.wikipedia.org/wiki/Heart" title="Heart">heart</a> to the smallest <a href="https://en.wikipedia.org/wiki/Capillaries" class="mw-redirect" title="Capillaries">capillaries</a>.
</p><p>These cells have unique functions that include <a href="https://en.wikipedia.org/wiki/Ultrafiltration" title="Ultrafiltration">fluid filtration</a>, such as in the <a href="https://en.wikipedia.org/wiki/Glomerulus" title="Glomerulus">glomerulus</a> of the kidney, <a href="https://en.wikipedia.org/wiki/Muscle_tone" 
title="Muscle tone">blood vessel tone</a>, <a href="https://en.wikipedia.org/wiki/Hemostasis" title="Hemostasis">hemostasis</a>, <a href="https://en.wikipedia.org/wiki/Neutrophil" title="Neutrophil">neutrophil</a> recruitment, and hormone trafficking. Endothelium of the interior surfaces of the heart 
chambers is called <a href="https://en.wikipedia.org/wiki/Endocardium" title="Endocardium">endocardium</a>. An impaired function can lead to serious health issues throughout the body.
</p>
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Endothelium">"Endothelium"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
elif cell=='BrainCell':
    des='''<p><b>Brain cells</b> make up the <a href="https://en.wikipedia.org/wiki/Parenchyma#Brain" title="Parenchyma">functional tissue of the brain</a>. The rest of the brain tissue is structural or connective called the <a href="https://en.wikipedia.org/wiki/Stroma_(tissue)" title="Stroma (tissue)">
    stroma</a> which includes <a href="https://en.wikipedia.org/wiki/Blood_vessel" title="Blood vessel">blood vessels</a>. The two main types of cells in the <a href="https://en.wikipedia.org/wiki/Brain" title="Brain">brain</a> are <a href="https://en.wikipedia.org/wiki/Neuron" title="Neuron">neurons</a>, also known as nerve cells, 
    and <a href="https://en.wikipedia.org/wiki/Glial_cell" class="mw-redirect" title="Glial cell">glial cells</a> also known as neuroglia.
</p><p>Neurons are the <a href="https://en.wikipedia.org/wiki/Excitable_cell" class="mw-redirect" title="Excitable cell">excitable cells</a> of the brain that function by communicating with other neurons and <a href="https://en.wikipedia.org/wiki/Interneuron" title="Interneuron">interneurons</a> 
(via <a href="https://en.wikipedia.org/wiki/Synapse" title="Synapse">synapses</a>), in <a href="https://en.wikipedia.org/wiki/Neural_circuit" title="Neural circuit">neural circuits</a> and <a href="https://en.wikipedia.org/wiki/Large-scale_brain_networks" class="mw-redirect" title="Large-scale brain networks">larger brain networks</a>.
 The two main neuronal classes in the <a href="https://en.wikipedia.org/wiki/Cerebral_cortex" title="Cerebral cortex">cerebral cortex</a> are excitatory projection neurons, and inhibitory interneurons; around 70-80 per cent are neurons, and 20-30 per cent inhibitory interneurons.
 Neurons are often grouped into a cluster known as a <a href="https://en.wikipedia.org/wiki/Nucleus_(neuroanatomy)" title="Nucleus (neuroanatomy)">nucleus</a> where they usually have 
 roughly similar connections and functions.Nuclei are connected to other nuclei by <a href="https://en.wikipedia.org/wiki/Nerve_tract" title="Nerve tract">tracts</a> of <a href="https://en.wikipedia.org/wiki/White_matter" 
 title="White matter">white matter</a>.
</p><p>Glia are the supporting cells of the neurons and have many functions not all of which are clearly understood, but include providing support and nutrients to the neurons. Glia are grouped into <a href="https://en.wikipedia.org/wiki/Macroglia" class="mw-redirect" 
title="Macroglia">macroglia</a> of <a href="https://en.wikipedia.org/wiki/Astrocyte" title="Astrocyte">astrocytes</a>, <a href="https://en.wikipedia.org/wiki/Ependymal_cell" class="mw-redirect" title="Ependymal cell">ependymal cells</a>, and <a href="https://en.wikipedia.org/wiki/Oligodendrocyte" title="Oligodendrocyte">oligodendrocytes</a>, 
and much smaller <a href="https://en.wikipedia.org/wiki/Microglia" title="Microglia">microglia</a>. Astrocytes are seen to be capable of communication with neurons involving a signalling process similar to <a href="https://en.wikipedia.org/wiki/Neurotransmission" title="Neurotransmission">neurotransmission</a> called
 <a href="https://en.wikipedia.org/wiki/Gliotransmitter" title="Gliotransmitter">gliotransmission</a>.
</p>
This article uses material from the Wikipedia article <a href="https://en.wikipedia.org/wiki/Brain_cell">"Brain cell"</a>, which is released under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share-Alike License 3.0</a>.
<link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1033289096">'''
elif cell=='RTE':
    des='''
    <p><b>Retrotransposons</b> (also called <b>Class I transposable elements</b> or <b>transposons via RNA intermediates</b>) are a type of
    genetic component that copy and paste themselves into different genomic locations (transposon) by converting RNA back into DNA through the reverse transcription
    process using an RNA transposition intermediate.
    <p>In scARE, we profiled RTE expression of <b>~850</b> subfamilies in over <b>600,000</b> cells, spanning <b>3</b> neurodegenerative diseases, including Alzheimer's disease, Parkinson's disease and multiple sclerosis.
    '''
elif cell=='AllDataset':
    des='''Summarization of all the dataset'''
# print(des.encode('utf-8'))
print(des)