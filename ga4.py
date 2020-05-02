import random
from operator import itemgetter
from matplotlib import pyplot as plt
import numpy as np

CXPB = 0.8 #交叉概率
MUTPB = 0.1 # 变异概率
NGEN = 1000 # 迭代次数
popsize  = 100 # 种群个体数
d = 5
# d = 10
# d = 30
# d = 50
lb = [-600 for _ in range(d)]
ub = [600 for _ in range(d)]
class Gene():
    '''
    gene: n维的数组
    '''
    def __init__(self, gene):
        self.gene = gene

class GA():

    '''
    初始化种群以及保存种群的最好个体
    '''
    def __init__(self):
        pop = []
        for i in range(popsize):
            individual = []
            for j in range(len(ub)):
                individual.append(random.randint(lb[j], ub[j]))
            fitness = self.evaluate(individual)
            pop.append({'Gene' : Gene(individual), 'fitness' : fitness})
        self.pop = pop
        self.bestIndividual = self.selectBest(pop)


    '''
    评估一个个体的好坏
    '''
    def evaluate(self, x):
        y1 = 0.0
        for i in range(d):
            y1 += x[i]**2/4000
        y2 = 1.0
        for i in range(d):
            y2 *= np.cos(x[i]/np.sqrt(i+1))
        return 10+100/(1+y1+y2)

    '''
    选择种群中最好的个体
    Pop：种群
    '''
    def selectBest(self, pop):
        s = sorted(pop, key=itemgetter('fitness'),reverse=True) # 按照适应度从大到小排列
        return s[0]

    '''
    选择
    pop:种群
    '''
    def selction(self, pop):

        sum_fit = sum(ind['fitness'] for ind in pop)
        chosen = []
        for i in range(popsize):
            fit = sum_fit * random.random()
            t = 0
            for ind in pop:
                t += ind['fitness']
                if t >= fit:
                    chosen.append(ind)
                    break
        chosen = sorted(chosen, key=itemgetter('fitness'), reverse=False) # 从小到大排序，因为pop方法会弹最后一个出来
        return chosen

    '''
    交叉：双点交叉
    offspring：两个个体
    '''
    def cross(self, offspring):
        dim = len(offspring[0]['Gene'].gene)
        gen1 = offspring[0]['Gene'].gene
        gen2 = offspring[1]['Gene'].gene

        if dim == 0:
            pos1 = 1
            pos2 = 1
        else:
            pos1 = random.randrange(1, dim) # 不能取到右区间端点
            pos2 = random.randrange(1, dim)

        newOff1 = Gene([])
        newOff2 = Gene([])
        temp1 = []
        temp2 = []
        for i in range(dim):
            if min(pos1, pos2) <= i < max(pos1, pos2):
                temp1.append(gen1[i])
                temp2.append(gen2[i])
            else:
                temp1.append(gen2[i])
                temp2.append(gen1[i])
        newOff1.gene = temp1
        newOff2.gene =  temp2
        f1 = self.evaluate(newOff1.gene)
        f2 = self.evaluate(newOff2.gene)
        return {'Gene':newOff1, 'fitness':f1}, {'Gene':newOff2, 'fitness':f2}

    '''
    变异
    individual：单个个体
    '''
    def mut(self, individual):
        dim = len(individual['Gene'].gene)
        if dim == 1:
            pos = 0
        else:
            pos = random.randrange(0, dim)
        individual['Gene'].gene[pos] = random.randint(lb[pos], ub[pos])
        individual['fitness'] = self.evaluate(individual['Gene'].gene)
        return individual

    def GA_main(self):
        all_y = []


        print('begin:')


        for g in range(NGEN):
            # print('------iter {}-------:'.format(g))

            selectPop = self.selction(self.pop)
            nextPop = []
            while len(nextPop) != popsize:
                offspring = [selectPop.pop() for _ in range(2)] # 取两个个体
                if random.random() <= CXPB: # 交叉
                    cf1, cf2 = self.cross(offspring)
                    if random.random() <= MUTPB:
                        mu1 = self.mut(cf1)
                        mu2 = self.mut(cf2)
                        nextPop.append(mu1)
                        nextPop.append(mu2)
                    else:
                        nextPop.append(cf1)
                        nextPop.append(cf2)
                else: # 
                    nextPop.extend(offspring)

            self.pop = nextPop
            bestIndividual = self.selectBest(self.pop)

            if bestIndividual['fitness'] > self.bestIndividual['fitness']:
                self.bestIndividual = bestIndividual
            
            if g == NGEN-1:
                print("bestindividual x: {}, fit:{}".format(self.bestIndividual['Gene'].gene, 100/(self.bestIndividual['fitness']-10)))
            all_y.append(100/(self.bestIndividual['fitness']-10))

        print('end!')        

        plt.xlabel('iteration:')
        plt.ylabel('y:')
        plt.plot(all_y)
        plt.show()

if __name__ == "__main__":
    ga = GA()
    ga.GA_main()
    