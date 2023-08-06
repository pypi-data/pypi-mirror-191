#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/include/builtins/assert.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/max.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/empty_like.hpp>
#include <pythonic/include/numpy/float64.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/eq.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/le.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mod.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/assert.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/max.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/empty_like.hpp>
#include <pythonic/numpy/float64.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/eq.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/le.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mod.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran__hessian_det_appx
{
  struct _clip
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
      typedef __type2 __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
      typedef __type4 __type5;
      typedef typename __combined<__type1,__type3,__type5>::type __type6;
      typedef typename pythonic::returnable<__type6>::type __type7;
      typedef __type7 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& x, argument_type1&& low, argument_type2&& high) const
    ;
  }  ;
  struct _integ
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    struct type
    {
      typedef _clip __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef __type1 __type2;
      typedef long __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
      typedef __type4 __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type5>())) __type6;
      typedef decltype(pythonic::types::as_const(std::declval<__type6>())) __type7;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type7>::type>::type __type8;
      typedef decltype(pythonic::operator_::sub(std::declval<__type8>(), std::declval<__type3>())) __type9;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>(), std::declval<__type9>())) __type10;
      typedef __type10 __type11;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type12;
      typedef __type12 __type13;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type7>::type>::type __type17;
      typedef decltype(pythonic::operator_::sub(std::declval<__type17>(), std::declval<__type3>())) __type18;
      typedef decltype(std::declval<__type0>()(std::declval<__type13>(), std::declval<__type3>(), std::declval<__type18>())) __type19;
      typedef __type19 __type20;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::max{})>::type>::type __type21;
      typedef double __type22;
      typedef decltype(pythonic::types::as_const(std::declval<__type5>())) __type24;
      typedef typename pythonic::assignable<__type10>::type __type25;
      typedef __type25 __type26;
      typedef typename pythonic::assignable<__type19>::type __type27;
      typedef __type27 __type28;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type26>(), std::declval<__type28>())) __type29;
      typedef decltype(std::declval<__type24>()[std::declval<__type29>()]) __type30;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type34;
      typedef __type34 __type35;
      typedef decltype(pythonic::operator_::add(std::declval<__type26>(), std::declval<__type35>())) __type36;
      typedef decltype(std::declval<__type0>()(std::declval<__type36>(), std::declval<__type3>(), std::declval<__type9>())) __type42;
      typedef typename pythonic::assignable<__type42>::type __type43;
      typedef __type43 __type44;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type46;
      typedef __type46 __type47;
      typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type47>())) __type48;
      typedef decltype(std::declval<__type0>()(std::declval<__type48>(), std::declval<__type3>(), std::declval<__type18>())) __type54;
      typedef typename pythonic::assignable<__type54>::type __type55;
      typedef __type55 __type56;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type44>(), std::declval<__type56>())) __type57;
      typedef decltype(std::declval<__type24>()[std::declval<__type57>()]) __type58;
      typedef decltype(pythonic::operator_::add(std::declval<__type30>(), std::declval<__type58>())) __type59;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type26>(), std::declval<__type56>())) __type64;
      typedef decltype(std::declval<__type24>()[std::declval<__type64>()]) __type65;
      typedef decltype(pythonic::operator_::sub(std::declval<__type59>(), std::declval<__type65>())) __type66;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type44>(), std::declval<__type28>())) __type71;
      typedef decltype(std::declval<__type24>()[std::declval<__type71>()]) __type72;
      typedef decltype(pythonic::operator_::sub(std::declval<__type66>(), std::declval<__type72>())) __type73;
      typedef typename __combined<__type22,__type73>::type __type74;
      typedef decltype(std::declval<__type21>()(std::declval<__type74>(), std::declval<__type73>())) __type75;
      typedef typename pythonic::returnable<__type75>::type __type76;
      typedef __type11 __ptype0;
      typedef __type20 __ptype1;
      typedef __type76 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    inline
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0&& img, argument_type1&& r, argument_type2&& c, argument_type3&& rl, argument_type4&& cl) const
    ;
  }  ;
  struct _hessian_matrix_det
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty_like{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef __type1 __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type3;
      typedef decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>())) __type4;
      typedef typename pythonic::assignable<__type4>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type6;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type8;
      typedef decltype(pythonic::types::as_const(std::declval<__type8>())) __type9;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type9>::type>::type __type10;
      typedef typename pythonic::lazy<__type10>::type __type11;
      typedef __type11 __type12;
      typedef decltype(std::declval<__type6>()(std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
      typedef __type14 __type15;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type9>::type>::type __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef __type17 __type18;
      typedef decltype(std::declval<__type6>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
      typedef __type20 __type21;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type15>(), std::declval<__type21>())) __type22;
      typedef indexable<__type22> __type23;
      typedef _integ __type24;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type27;
      typedef long __type28;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type29;
      typedef __type29 __type30;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type30>())) __type31;
      typedef decltype(std::declval<__type27>()(std::declval<__type31>())) __type32;
      typedef typename pythonic::assignable<__type32>::type __type33;
      typedef __type33 __type34;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type34>(), std::declval<__type28>())) __type35;
      typedef typename pythonic::assignable<__type35>::type __type36;
      typedef __type36 __type37;
      typedef decltype(pythonic::operator_::sub(std::declval<__type15>(), std::declval<__type37>())) __type38;
      typedef decltype(pythonic::operator_::add(std::declval<__type38>(), std::declval<__type28>())) __type39;
      typedef decltype(pythonic::operator_::sub(std::declval<__type34>(), std::declval<__type28>())) __type42;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type42>(), std::declval<__type28>())) __type43;
      typedef typename pythonic::assignable<__type43>::type __type44;
      typedef __type44 __type45;
      typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type45>())) __type46;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type37>())) __type48;
      typedef decltype(pythonic::operator_::sub(std::declval<__type48>(), std::declval<__type28>())) __type49;
      typedef typename pythonic::assignable<__type34>::type __type51;
      typedef typename __combined<__type51,__type28>::type __type52;
      typedef __type52 __type53;
      typedef typename _integ::type<__type2, __type39, __type46, __type49, __type53>::__ptype0 __type54;
      typedef typename __combined<__type39,__type54>::type __type55;
      typedef typename _integ::type<__type2, __type55, __type46, __type49, __type53>::__ptype1 __type56;
      typedef typename __combined<__type46,__type56>::type __type57;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type55>(), std::declval<__type57>(), std::declval<__type49>(), std::declval<__type53>())) __type58;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type37>(), std::declval<__type28>())) __type66;
      typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type66>())) __type67;
      typedef typename _integ::type<__type2, __type39, __type67, __type49, __type37>::__ptype0 __type72;
      typedef typename __combined<__type39,__type72>::type __type73;
      typedef typename _integ::type<__type2, __type73, __type67, __type49, __type37>::__ptype1 __type74;
      typedef typename __combined<__type67,__type74>::type __type75;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type73>(), std::declval<__type75>(), std::declval<__type49>(), std::declval<__type37>())) __type76;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type76>())) __type77;
      typedef decltype(pythonic::operator_::sub(std::declval<__type58>(), std::declval<__type77>())) __type78;
      typedef decltype(pythonic::operator_::neg(std::declval<__type78>())) __type79;
      typedef double __type80;
      typedef typename __combined<__type33,__type34>::type __type81;
      typedef __type81 __type82;
      typedef decltype(pythonic::operator_::div(std::declval<__type80>(), std::declval<__type82>())) __type83;
      typedef decltype(pythonic::operator_::div(std::declval<__type83>(), std::declval<__type82>())) __type85;
      typedef typename pythonic::assignable<__type85>::type __type86;
      typedef __type86 __type87;
      typedef decltype(pythonic::operator_::mul(std::declval<__type79>(), std::declval<__type87>())) __type88;
      typedef decltype(pythonic::operator_::sub(std::declval<__type15>(), std::declval<__type45>())) __type92;
      typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type37>())) __type95;
      typedef decltype(pythonic::operator_::add(std::declval<__type95>(), std::declval<__type28>())) __type96;
      typedef typename _integ::type<__type2, __type92, __type96, __type53, __type49>::__ptype0 __type101;
      typedef typename __combined<__type92,__type101>::type __type102;
      typedef typename _integ::type<__type2, __type102, __type96, __type53, __type49>::__ptype1 __type103;
      typedef typename __combined<__type96,__type103>::type __type104;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type102>(), std::declval<__type104>(), std::declval<__type53>(), std::declval<__type49>())) __type105;
      typedef decltype(pythonic::operator_::sub(std::declval<__type15>(), std::declval<__type66>())) __type110;
      typedef typename _integ::type<__type2, __type110, __type96, __type37, __type49>::__ptype0 __type119;
      typedef typename __combined<__type110,__type119>::type __type120;
      typedef typename _integ::type<__type2, __type120, __type96, __type37, __type49>::__ptype1 __type121;
      typedef typename __combined<__type96,__type121>::type __type122;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type120>(), std::declval<__type122>(), std::declval<__type37>(), std::declval<__type49>())) __type123;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type123>())) __type124;
      typedef decltype(pythonic::operator_::sub(std::declval<__type105>(), std::declval<__type124>())) __type125;
      typedef decltype(pythonic::operator_::neg(std::declval<__type125>())) __type126;
      typedef decltype(pythonic::operator_::mul(std::declval<__type126>(), std::declval<__type87>())) __type128;
      typedef decltype(pythonic::operator_::mul(std::declval<__type88>(), std::declval<__type128>())) __type129;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type130;
      typedef decltype(pythonic::operator_::add(std::declval<__type21>(), std::declval<__type28>())) __type136;
      typedef typename _integ::type<__type2, __type38, __type136, __type37, __type37>::__ptype0 __type139;
      typedef typename __combined<__type38,__type139>::type __type140;
      typedef typename _integ::type<__type2, __type140, __type136, __type37, __type37>::__ptype1 __type141;
      typedef typename __combined<__type136,__type141>::type __type142;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type140>(), std::declval<__type142>(), std::declval<__type37>(), std::declval<__type37>())) __type143;
      typedef decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type28>())) __type146;
      typedef typename _integ::type<__type2, __type146, __type95, __type37, __type37>::__ptype0 __type152;
      typedef typename __combined<__type146,__type152>::type __type153;
      typedef typename _integ::type<__type2, __type153, __type95, __type37, __type37>::__ptype1 __type154;
      typedef typename __combined<__type95,__type154>::type __type155;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type153>(), std::declval<__type155>(), std::declval<__type37>(), std::declval<__type37>())) __type156;
      typedef decltype(pythonic::operator_::add(std::declval<__type143>(), std::declval<__type156>())) __type157;
      typedef typename _integ::type<__type2, __type38, __type95, __type37, __type37>::__ptype0 __type167;
      typedef typename __combined<__type38,__type167>::type __type168;
      typedef typename _integ::type<__type2, __type168, __type95, __type37, __type37>::__ptype1 __type169;
      typedef typename __combined<__type95,__type169>::type __type170;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type168>(), std::declval<__type170>(), std::declval<__type37>(), std::declval<__type37>())) __type171;
      typedef decltype(pythonic::operator_::sub(std::declval<__type157>(), std::declval<__type171>())) __type172;
      typedef typename _integ::type<__type2, __type146, __type136, __type37, __type37>::__ptype0 __type180;
      typedef typename __combined<__type146,__type180>::type __type181;
      typedef typename _integ::type<__type2, __type181, __type136, __type37, __type37>::__ptype1 __type182;
      typedef typename __combined<__type136,__type182>::type __type183;
      typedef decltype(std::declval<__type24>()(std::declval<__type2>(), std::declval<__type181>(), std::declval<__type183>(), std::declval<__type37>(), std::declval<__type37>())) __type184;
      typedef decltype(pythonic::operator_::sub(std::declval<__type172>(), std::declval<__type184>())) __type185;
      typedef decltype(pythonic::operator_::neg(std::declval<__type185>())) __type186;
      typedef decltype(pythonic::operator_::mul(std::declval<__type186>(), std::declval<__type87>())) __type188;
      typedef decltype(std::declval<__type130>()(std::declval<__type188>())) __type189;
      typedef decltype(pythonic::operator_::mul(std::declval<__type80>(), std::declval<__type189>())) __type190;
      typedef decltype(pythonic::operator_::sub(std::declval<__type129>(), std::declval<__type190>())) __type191;
      typedef container<typename std::remove_reference<__type191>::type> __type192;
      typedef typename __combined<__type5,__type23,__type192>::type __type193;
      typedef __type193 __type194;
      typedef typename pythonic::returnable<__type194>::type __type195;
      typedef __type195 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& img, argument_type1&& sigma) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename _clip::type<argument_type0, argument_type1, argument_type2>::result_type _clip::operator()(argument_type0&& x, argument_type1&& low, argument_type2&& high) const
  {
    pythonic::pythran_assert(pythonic::operator_::le(0L, low) and pythonic::operator_::le(low, high));
    if (pythonic::operator_::gt(x, high))
    {
      return high;
    }
    else
    {
      if (pythonic::operator_::lt(x, low))
      {
        return low;
      }
      else
      {
        return x;
      }
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
  inline
  typename _integ::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type _integ::operator()(argument_type0&& img, argument_type1&& r, argument_type2&& c, argument_type3&& rl, argument_type4&& cl) const
  {
    typename pythonic::assignable_noescape<decltype(_clip()(r, 0L, pythonic::operator_::sub(std::get<0>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L)))>::type r__ = _clip()(r, 0L, pythonic::operator_::sub(std::get<0>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L));
    typename pythonic::assignable_noescape<decltype(_clip()(c, 0L, pythonic::operator_::sub(std::get<1>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L)))>::type c__ = _clip()(c, 0L, pythonic::operator_::sub(std::get<1>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L));
    typename pythonic::assignable_noescape<decltype(_clip()(pythonic::operator_::add(r__, rl), 0L, pythonic::operator_::sub(std::get<0>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L)))>::type r2 = _clip()(pythonic::operator_::add(r__, rl), 0L, pythonic::operator_::sub(std::get<0>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L));
    typename pythonic::assignable_noescape<decltype(_clip()(pythonic::operator_::add(c__, cl), 0L, pythonic::operator_::sub(std::get<1>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L)))>::type c2 = _clip()(pythonic::operator_::add(c__, cl), 0L, pythonic::operator_::sub(std::get<1>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))), 1L));
    return pythonic::builtins::functor::max{}(0.0, pythonic::operator_::sub(pythonic::operator_::sub(pythonic::operator_::add(pythonic::types::as_const(img).fast(pythonic::types::make_tuple(r__, c__)), pythonic::types::as_const(img).fast(pythonic::types::make_tuple(r2, c2))), pythonic::types::as_const(img).fast(pythonic::types::make_tuple(r__, c2))), pythonic::types::as_const(img).fast(pythonic::types::make_tuple(r2, c__))));
  }
  template <typename argument_type0 , typename argument_type1 >
  inline
  typename _hessian_matrix_det::type<argument_type0, argument_type1>::result_type _hessian_matrix_det::operator()(argument_type0&& img, argument_type1&& sigma) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type0;
    typedef long __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
    typedef __type2 __type3;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type3>())) __type4;
    typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
    typedef typename pythonic::assignable<__type5>::type __type6;
    typedef __type6 __type7;
    typedef typename __combined<__type6,__type7,__type1>::type __type8;
    typedef typename pythonic::assignable<__type8>::type __type9;
    typedef typename pythonic::assignable<__type7>::type __type10;
    typedef typename __combined<__type10,__type1>::type __type11;
    typedef typename pythonic::assignable<__type11>::type __type12;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty_like{})>::type>::type __type13;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type14;
    typedef __type14 __type15;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float64{})>::type>::type __type16;
    typedef decltype(std::declval<__type13>()(std::declval<__type15>(), std::declval<__type16>())) __type17;
    typedef typename pythonic::assignable<__type17>::type __type18;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type19;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type15>())) __type21;
    typedef decltype(pythonic::types::as_const(std::declval<__type21>())) __type22;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type22>::type>::type __type23;
    typedef typename pythonic::lazy<__type23>::type __type24;
    typedef __type24 __type25;
    typedef decltype(std::declval<__type19>()(std::declval<__type25>())) __type26;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type26>::type::iterator>::value_type>::type __type27;
    typedef __type27 __type28;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type22>::type>::type __type29;
    typedef typename pythonic::lazy<__type29>::type __type30;
    typedef __type30 __type31;
    typedef decltype(std::declval<__type19>()(std::declval<__type31>())) __type32;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type __type33;
    typedef __type33 __type34;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type28>(), std::declval<__type34>())) __type35;
    typedef indexable<__type35> __type36;
    typedef _integ __type37;
    typedef __type8 __type40;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type40>(), std::declval<__type1>())) __type41;
    typedef typename pythonic::assignable<__type41>::type __type42;
    typedef __type42 __type43;
    typedef decltype(pythonic::operator_::sub(std::declval<__type28>(), std::declval<__type43>())) __type44;
    typedef decltype(pythonic::operator_::add(std::declval<__type44>(), std::declval<__type1>())) __type45;
    typedef decltype(pythonic::operator_::sub(std::declval<__type40>(), std::declval<__type1>())) __type48;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type48>(), std::declval<__type1>())) __type49;
    typedef typename pythonic::assignable<__type49>::type __type50;
    typedef __type50 __type51;
    typedef decltype(pythonic::operator_::sub(std::declval<__type34>(), std::declval<__type51>())) __type52;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type43>())) __type54;
    typedef decltype(pythonic::operator_::sub(std::declval<__type54>(), std::declval<__type1>())) __type55;
    typedef __type11 __type56;
    typedef typename _integ::type<__type15, __type45, __type52, __type55, __type56>::__ptype0 __type57;
    typedef typename __combined<__type45,__type57>::type __type58;
    typedef typename _integ::type<__type15, __type58, __type52, __type55, __type56>::__ptype1 __type59;
    typedef typename __combined<__type52,__type59>::type __type60;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type58>(), std::declval<__type60>(), std::declval<__type55>(), std::declval<__type56>())) __type61;
    typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type43>(), std::declval<__type1>())) __type69;
    typedef decltype(pythonic::operator_::sub(std::declval<__type34>(), std::declval<__type69>())) __type70;
    typedef typename _integ::type<__type15, __type45, __type70, __type55, __type43>::__ptype0 __type75;
    typedef typename __combined<__type45,__type75>::type __type76;
    typedef typename _integ::type<__type15, __type76, __type70, __type55, __type43>::__ptype1 __type77;
    typedef typename __combined<__type70,__type77>::type __type78;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type76>(), std::declval<__type78>(), std::declval<__type55>(), std::declval<__type43>())) __type79;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type79>())) __type80;
    typedef decltype(pythonic::operator_::sub(std::declval<__type61>(), std::declval<__type80>())) __type81;
    typedef decltype(pythonic::operator_::neg(std::declval<__type81>())) __type82;
    typedef double __type83;
    typedef decltype(pythonic::operator_::div(std::declval<__type83>(), std::declval<__type40>())) __type85;
    typedef decltype(pythonic::operator_::div(std::declval<__type85>(), std::declval<__type40>())) __type87;
    typedef typename pythonic::assignable<__type87>::type __type88;
    typedef __type88 __type89;
    typedef decltype(pythonic::operator_::mul(std::declval<__type82>(), std::declval<__type89>())) __type90;
    typedef decltype(pythonic::operator_::sub(std::declval<__type28>(), std::declval<__type51>())) __type94;
    typedef decltype(pythonic::operator_::sub(std::declval<__type34>(), std::declval<__type43>())) __type97;
    typedef decltype(pythonic::operator_::add(std::declval<__type97>(), std::declval<__type1>())) __type98;
    typedef typename _integ::type<__type15, __type94, __type98, __type56, __type55>::__ptype0 __type103;
    typedef typename __combined<__type94,__type103>::type __type104;
    typedef typename _integ::type<__type15, __type104, __type98, __type56, __type55>::__ptype1 __type105;
    typedef typename __combined<__type98,__type105>::type __type106;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type104>(), std::declval<__type106>(), std::declval<__type56>(), std::declval<__type55>())) __type107;
    typedef decltype(pythonic::operator_::sub(std::declval<__type28>(), std::declval<__type69>())) __type112;
    typedef typename _integ::type<__type15, __type112, __type98, __type43, __type55>::__ptype0 __type121;
    typedef typename __combined<__type112,__type121>::type __type122;
    typedef typename _integ::type<__type15, __type122, __type98, __type43, __type55>::__ptype1 __type123;
    typedef typename __combined<__type98,__type123>::type __type124;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type122>(), std::declval<__type124>(), std::declval<__type43>(), std::declval<__type55>())) __type125;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type125>())) __type126;
    typedef decltype(pythonic::operator_::sub(std::declval<__type107>(), std::declval<__type126>())) __type127;
    typedef decltype(pythonic::operator_::neg(std::declval<__type127>())) __type128;
    typedef decltype(pythonic::operator_::mul(std::declval<__type128>(), std::declval<__type89>())) __type130;
    typedef decltype(pythonic::operator_::mul(std::declval<__type90>(), std::declval<__type130>())) __type131;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type132;
    typedef decltype(pythonic::operator_::add(std::declval<__type34>(), std::declval<__type1>())) __type138;
    typedef typename _integ::type<__type15, __type44, __type138, __type43, __type43>::__ptype0 __type141;
    typedef typename __combined<__type44,__type141>::type __type142;
    typedef typename _integ::type<__type15, __type142, __type138, __type43, __type43>::__ptype1 __type143;
    typedef typename __combined<__type138,__type143>::type __type144;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type142>(), std::declval<__type144>(), std::declval<__type43>(), std::declval<__type43>())) __type145;
    typedef decltype(pythonic::operator_::add(std::declval<__type28>(), std::declval<__type1>())) __type148;
    typedef typename _integ::type<__type15, __type148, __type97, __type43, __type43>::__ptype0 __type154;
    typedef typename __combined<__type148,__type154>::type __type155;
    typedef typename _integ::type<__type15, __type155, __type97, __type43, __type43>::__ptype1 __type156;
    typedef typename __combined<__type97,__type156>::type __type157;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type155>(), std::declval<__type157>(), std::declval<__type43>(), std::declval<__type43>())) __type158;
    typedef decltype(pythonic::operator_::add(std::declval<__type145>(), std::declval<__type158>())) __type159;
    typedef typename _integ::type<__type15, __type44, __type97, __type43, __type43>::__ptype0 __type169;
    typedef typename __combined<__type44,__type169>::type __type170;
    typedef typename _integ::type<__type15, __type170, __type97, __type43, __type43>::__ptype1 __type171;
    typedef typename __combined<__type97,__type171>::type __type172;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type170>(), std::declval<__type172>(), std::declval<__type43>(), std::declval<__type43>())) __type173;
    typedef decltype(pythonic::operator_::sub(std::declval<__type159>(), std::declval<__type173>())) __type174;
    typedef typename _integ::type<__type15, __type148, __type138, __type43, __type43>::__ptype0 __type182;
    typedef typename __combined<__type148,__type182>::type __type183;
    typedef typename _integ::type<__type15, __type183, __type138, __type43, __type43>::__ptype1 __type184;
    typedef typename __combined<__type138,__type184>::type __type185;
    typedef decltype(std::declval<__type37>()(std::declval<__type15>(), std::declval<__type183>(), std::declval<__type185>(), std::declval<__type43>(), std::declval<__type43>())) __type186;
    typedef decltype(pythonic::operator_::sub(std::declval<__type174>(), std::declval<__type186>())) __type187;
    typedef decltype(pythonic::operator_::neg(std::declval<__type187>())) __type188;
    typedef decltype(pythonic::operator_::mul(std::declval<__type188>(), std::declval<__type89>())) __type190;
    typedef decltype(std::declval<__type132>()(std::declval<__type190>())) __type191;
    typedef decltype(pythonic::operator_::mul(std::declval<__type83>(), std::declval<__type191>())) __type192;
    typedef decltype(pythonic::operator_::sub(std::declval<__type131>(), std::declval<__type192>())) __type193;
    typedef container<typename std::remove_reference<__type193>::type> __type194;
    typedef typename __combined<__type18,__type36,__type194>::type __type195;
    typedef typename pythonic::assignable<__type195>::type __type196;
    __type9 size = pythonic::builtins::functor::int_{}(pythonic::operator_::mul(3L, sigma));
    typename pythonic::lazy<decltype(std::get<0>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))))>::type height = std::get<0>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img)));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img))))>::type width = std::get<1>(pythonic::types::as_const(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, img)));
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(pythonic::operator_::sub(size, 1L), 2L))>::type s2 = pythonic::operator_::functor::floordiv()(pythonic::operator_::sub(size, 1L), 2L);
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(size, 3L))>::type s3 = pythonic::operator_::functor::floordiv()(size, 3L);
    __type12 w = size;
    __type196 out = pythonic::numpy::functor::empty_like{}(img, pythonic::numpy::functor::float64{});
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::div(pythonic::operator_::div(1.0, size), size))>::type w_i = pythonic::operator_::div(pythonic::operator_::div(1.0, size), size);
    if (pythonic::operator_::eq(pythonic::operator_::mod(size, 2L), 0L))
    {
      size += 1L;
    }
    {
      long  __target140357413005488 = height;
      for (long  r=0L; r < __target140357413005488; r += 1L)
      {
        {
          long  __target140357413020096 = width;
          for (long  c=0L; c < __target140357413020096; c += 1L)
          {
            out.fast(pythonic::types::make_tuple(r, c)) = pythonic::operator_::sub(pythonic::operator_::mul(pythonic::operator_::mul(pythonic::operator_::neg(pythonic::operator_::sub(_integ()(img, pythonic::operator_::add(pythonic::operator_::sub(r, s3), 1L), pythonic::operator_::sub(c, s2), pythonic::operator_::sub(pythonic::operator_::mul(2L, s3), 1L), w), pythonic::operator_::mul(3L, _integ()(img, pythonic::operator_::add(pythonic::operator_::sub(r, s3), 1L), pythonic::operator_::sub(c, pythonic::operator_::functor::floordiv()(s3, 2L)), pythonic::operator_::sub(pythonic::operator_::mul(2L, s3), 1L), s3)))), w_i), pythonic::operator_::mul(pythonic::operator_::neg(pythonic::operator_::sub(_integ()(img, pythonic::operator_::sub(r, s2), pythonic::operator_::add(pythonic::operator_::sub(c, s3), 1L), w, pythonic::operator_::sub(pythonic::operator_::mul(2L, s3), 1L)), pythonic::operator_::mul(3L, _integ()(img, pythonic::operator_::sub(r, pythonic::operator_::functor::floordiv()(s3, 2L)), pythonic::operator_::add(pythonic::operator_::sub(c, s3), 1L), s3, pythonic::operator_::sub(pythonic::operator_::mul(2L, s3), 1L))))), w_i)), pythonic::operator_::mul(0.81, pythonic::numpy::functor::square{}(pythonic::operator_::mul(pythonic::operator_::neg(pythonic::operator_::sub(pythonic::operator_::sub(pythonic::operator_::add(_integ()(img, pythonic::operator_::sub(r, s3), pythonic::operator_::add(c, 1L), s3, s3), _integ()(img, pythonic::operator_::add(r, 1L), pythonic::operator_::sub(c, s3), s3, s3)), _integ()(img, pythonic::operator_::sub(r, s3), pythonic::operator_::sub(c, s3), s3, s3)), _integ()(img, pythonic::operator_::add(r, 1L), pythonic::operator_::add(c, 1L), s3, s3))), w_i))));
          }
        }
      }
    }
    return out;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
inline
typename __pythran__hessian_det_appx::_hessian_matrix_det::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, double>::result_type _hessian_matrix_det0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& img, double&& sigma) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hessian_det_appx::_hessian_matrix_det()(img, sigma);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hessian_det_appx::_hessian_matrix_det::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, long>::result_type _hessian_matrix_det1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& img, long&& sigma) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hessian_det_appx::_hessian_matrix_det()(img, sigma);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hessian_det_appx::_hessian_matrix_det::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, double>::result_type _hessian_matrix_det2(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& img, double&& sigma) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hessian_det_appx::_hessian_matrix_det()(img, sigma);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran__hessian_det_appx::_hessian_matrix_det::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>, long>::result_type _hessian_matrix_det3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>&& img, long&& sigma) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran__hessian_det_appx::_hessian_matrix_det()(img, sigma);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap__hessian_matrix_det0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"img", "sigma",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<double>(args_obj[1]))
        return to_python(_hessian_matrix_det0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<double>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__hessian_matrix_det1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"img", "sigma",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(_hessian_matrix_det1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__hessian_matrix_det2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"img", "sigma",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<double>(args_obj[1]))
        return to_python(_hessian_matrix_det2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<double>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap__hessian_matrix_det3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"img", "sigma",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(_hessian_matrix_det3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall__hessian_matrix_det(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap__hessian_matrix_det0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__hessian_matrix_det1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__hessian_matrix_det2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap__hessian_matrix_det3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "_hessian_matrix_det", "\n""    - _hessian_matrix_det(float64[:,:], float)\n""    - _hessian_matrix_det(float64[:,:], int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "_hessian_matrix_det",
    (PyCFunction)__pythran_wrapall__hessian_matrix_det,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the approximate Hessian Determinant over a 2D image.\n""\n""    Supported prototypes:\n""\n""    - _hessian_matrix_det(float64[:,:], float)\n""    - _hessian_matrix_det(float64[:,:], int)\n""\n""    This method uses box filters over integral images to compute the\n""    approximate Hessian Determinant as described in [1]_.\n""\n""    Parameters\n""    ----------\n""    img : array\n""        The integral image over which to compute Hessian Determinant.\n""    sigma : float\n""        Standard deviation used for the Gaussian kernel, used for the Hessian\n""        matrix\n""\n""    Returns\n""    -------\n""    out : array\n""        The array of the Determinant of Hessians.\n""\n""    References\n""    ----------\n""    .. [1] Herbert Bay, Andreas Ess, Tinne Tuytelaars, Luc Van Gool,\n""           \"SURF: Speeded Up Robust Features\"\n""           ftp://ftp.vision.ee.ethz.ch/publications/articles/eth_biwi_00517.pdf\n""\n""    Notes\n""    -----\n""    The running time of this method only depends on size of the image. It is\n""    independent of `sigma` as one would expect. The downside is that the\n""    result for `sigma` less than `3` is not accurate, i.e., not similar to\n""    the result obtained if someone computed the Hessian and took its\n""    determinant.\n"""},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_hessian_det_appx",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_hessian_det_appx)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(_hessian_det_appx)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("_hessian_det_appx",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.12.1",
                                      "2023-02-13 19:43:57.255759",
                                      "111df3f05b1722c5922142a30a883be28dd42292a0cb704a6f287101ad47f83c");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif