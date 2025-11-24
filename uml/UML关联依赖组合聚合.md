#uml
#关联依赖
#组合聚合
## 关联关系和依赖关系什么区别
```java
// 关联关系 
// 持久的 类级别的行用
public class student ｛
    // Teacher是student的一个属性 长期持有
    private Teacher teacher; // 关联关系
}
```

```java
// 依赖关系 
// 临时性的 通常在方法中使用
public class OrderService {
    public void createOrder (User user) ｛ // 依赖关系
        // user只在方法中临时使用
    ｝
}
```
## 组合关系和聚合关系有什么差别

```java
// 组合关系
// 整体与部分的关系 部分不能独立存在
public class Car ｛ 
    private Engine engine;

    public Car() ｛
        engine = new Engine();
    ｝
｝
```

```java
// 聚合关系
// 整体与部分的关系部分可以独立存在
public class Department ｛ 
    private List <Employee> employees; // 部门和员工是聚合系
｝
```
